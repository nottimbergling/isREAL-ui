import matplotlib.pyplot as plt
import random
import numpy as np
from sklearn import datasets, linear_model
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from backend.nlp.hackaton_trainer import keywords
from backend.nlp.hackaton_trainer import statuses_to_stats
from backend.nlp.hackaton_trainer import statuses_to_ratings

texts_train = ['israel anti hamas bla bla', 'lol lol pwn lol',
         '1337 lol israel israel the best', 'anti-israel no no israel',
         'israel kills palestinats', 'alla akbar anti israel', 'boycott israel you suckers', 'fuck israel', 'flowers nice israel',
               ]
vec_new = 'anti-israel no no hamas alla akbar'
texts_train_score = [1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0]

def text_to_vector(txt):
    '''
    words = ['israel', 'salam', 'hamas', 'anti-israel',
             'no', 'yes', 'anti', 'alla', 'boycott',
             'freepalestine', 'anti israel', 'antisrael']
    '''
    vec = [txt.lower().count(word) for word in keywords]
    return vec

def vectors_to_training(vecs, known_scores):
    return vecs, list(map(lambda x: 1.0 if x else 0.0, known_scores))

def get_model(tr_set):
    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(*tr_set)
    return regr

def get_anti_israel_model(texts_train=texts_train, texts_train_score=texts_train_score):
    vecs = []
    for text in texts_train:
        vec = text_to_vector(text)
        vecs.append(vec)

    tr = vectors_to_training(vecs, texts_train_score)
    regr = get_model(tr)
    prediction = regr.predict([text_to_vector(vec_new)])
    print("Generated anti-israel model, predicting for new sample text.")
    print(vec_new, prediction)
    return regr


def get_exposure_model(features, scores):
    # features is vectors-array where each vector is: (likes, retwits, followers).
    tr = vectors_to_training(features, scores)
    regr = get_model(tr)
    print("Generated exposure-model.")
    return regr


def get_features(original_ftrs):
    ai_ft = list(map(text_to_vector, [original_ftrs[tid][0] for tid in original_ftrs]))
    exp_ft = [original_ftrs[tid][1:] for tid in original_ftrs]
    return (ai_ft, exp_ft)


def get_knn_model(x_test, x_tr=statuses_to_stats, x_sc=statuses_to_ratings):
    '''
    :param x_tr:  x training is a dict where for each twitter-id -> (twitter_text, likes, retwits, followers)
    :param x_sc:  x score is a dict where for each twitter-id -> (twitter_anti_israel_score, twitter_exposure_score, twitter_total_score_for_tweet)
    :return: for the x_test (same format as the x-training), the new ranking and scores for them. (in the future we can redo the kNN with new best ones, and stabilize it more
            we can also improve the other regressions before with more data if available).
    '''
    ai_tr, ai_sc = [x_tr[tid][0] for tid in x_tr], [x_sc[tid][0] for tid in x_sc]
    exp_tr, exp_sc = [x_tr[tid][1:] for tid in x_tr], [x_sc[tid][1] for tid in x_sc]
    ai_regr = get_anti_israel_model(ai_tr, ai_sc)
    ai_tr_res = np.maximum(np.minimum(ai_regr.predict(list(map(text_to_vector, ai_tr))), 5), 0)
    exp_regr = get_exposure_model(exp_tr, exp_sc)
    exp_tr_res = np.maximum(np.minimum(exp_regr.predict(exp_tr), 5), 0)
    assert len(exp_tr_res) == len(ai_tr_res)
    knn_tr_features, knn_tr_scores = list(zip(ai_tr_res, exp_tr_res)), [x_sc[tid][2] for tid in x_sc]
    knn = KNeighborsRegressor(n_neighbors=4)
    knn.fit(knn_tr_features, knn_tr_scores)
    ai_ft, exp_ft = get_features(x_test)
    ai_test_res, exp_test_res = np.maximum(np.minimum(ai_regr.predict(ai_ft), 5), 0), np.maximum(np.minimum(exp_regr.predict(exp_ft), 5), 0)
    x_test_features = list(zip(ai_test_res, exp_test_res))
    res = knn.predict(x_test_features)
    x_test_keys_to_ind = dict(list(zip(x_test.keys(), range(len(x_test.keys())))))
    best_twitsids = sorted(x_test.keys(), key=lambda x: res[x_test_keys_to_ind[x]], reverse=True)#[::-1]
    return best_twitsids  #, [x_test[cid][0] for cid in best_twitsids]


def split_datas(stats, rates):
    ids = stats.keys()
    res = []
    for i in range(10):
        tr_keys = random.sample(ids, 40)
        te_keys = set(ids) - set(tr_keys)
        tr_set = dict([(stat, stats[stat]) for stat in tr_keys])
        tr_sc_set = dict([(stat, rates[stat]) for stat in tr_keys])
        te_set = dict([(stat, stats[stat]) for stat in te_keys])
        te_sc_set = dict([(stat, rates[stat]) for stat in te_keys])
        te_sc_predict = get_knn_model(tr_set, tr_sc_set, te_set)
        print("top 5 are:", te_sc_predict[1][:5])
        res.append(te_sc_predict[1][:5])
    return res

'''
# Load the diabetes dataset
diabetes = datasets.load_diabetes()


# Use only one feature
diabetes_X = diabetes.data[:, np.newaxis, 2]

# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]

# Split the targets into training/testing sets
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)

# Make predictions using the testing set
diabetes_y_pred = regr.predict(diabetes_X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))

# Plot outputs
plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
plt.plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
'''