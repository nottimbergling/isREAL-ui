from backend import peachme

app = peachme.app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True, use_reloader=True)
