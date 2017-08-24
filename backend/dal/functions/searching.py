from datetime import date

from backend.dal.functions.lectures_and_users import get_lectures, get_users
from backend.dal.mongo_client.mongodb_client import mongo_connection, get_all_documents_from_collection, run_function
from backend.dal.functions.spaces_and_instances import get_my_spaces, get_instances_for_space


def get_all_visible_lectures(username):
    lectures = get_lectures()

    users = get_users()

    for lecture in lectures:
        for user in users:
            if user["username"] == lecture["username"]:
                lecture["user"] = user
                continue

    my_spaces = get_my_spaces(username)
    my_instances = []


    for space in my_spaces:
        space_instances = get_instances_for_space(space["_id"])
        for instance in space_instances:
            my_instances.append(instance)


    for current_instance in my_instances:
        for lecture in lectures:
            if (lecture["_id"] == current_instance["lecture_id"]):
                    lecture["instances"] = current_instance


    return lectures



def _add_distinctly_to_list(list,object):
    if object not in list:
        list.append(object)

def get_exact_search_results(username, users=None, tags=None, free_text=None):
    lectures_set = get_all_visible_lectures(username)

    for lecture in lectures_set:
        # find lecures with all of the tags
        if tags != None :
            for tag in tags:
                if tag not in lecture["tags"] and tag in lecture["user"]["tags"]:
                    lectures_set.remove(lecture)
                    continue

        # find lectures of one of the users
        if users != None :
            if lecture["user"]["username"] not in users:
                lectures_set.remove(lecture)
                continue

        # find lectures with one of the words
        if free_text != None :
            for word in free_text:
                if word not in lecture["description"] \
                        and word not in lecture["user"]["description"] \
                        and word != lecture["user"]["username"] \
                        and word not in lecture["tags"] \
                        and word not in lecture["category"]:
                    is_found_in_user_tags =False
                    for user_tag in lecture["user"]["tags"]:
                        if word == user_tag["name"]:
                            is_found_in_user_tags=True
                            break
                    if not is_found_in_user_tags:
                        lectures_set.remove(lecture)
                        continue

    return {"lectures": lectures_set}


def get_approximated_search_results(username, users, tags, free_text):
    lectures_set = []

    all_lectures = get_all_visible_lectures(username)

    for lecture in all_lectures:
        # find lecures with one of the tags
        for tag in tags:
            if tag in lecture["tags"]:
                _add_distinctly_to_list(lectures_set,lecture)
                break
            for user_tag in lecture["user"]["tags"]:
                if tag == user_tag["name"]:
                    _add_distinctly_to_list(lectures_set,lecture)
                    break

        # find lectures of one of the users
        for user in users:
            if user == lecture["user"]["username"]:
                _add_distinctly_to_list(lectures_set,lecture)
                break

        # find lectures with one of the words
        for word in free_text:
            if word in lecture["description"]:
                _add_distinctly_to_list(lectures_set,lecture)
                break
            if word in lecture["category"]:
                _add_distinctly_to_list(lectures_set,lecture)
                break
            if word in lecture["user"]["display_name"]:
                _add_distinctly_to_list(lectures_set,lecture)
                break
            if word == lecture["user"]["username"]:
                _add_distinctly_to_list(lectures_set,lecture)
                break
            if word in lecture["tags"]:
                _add_distinctly_to_list(lectures_set,lecture)
                break
            if lecture["user"]["tags"] is not None:
                for user_tag in lecture["user"]["tags"]:
                    if word == user_tag["name"]:
                        _add_distinctly_to_list(lectures_set,lecture)
                        break

    return {"lectures": lectures_set}
