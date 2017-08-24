from backend import peachme

app = peachme.app

if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=True)
