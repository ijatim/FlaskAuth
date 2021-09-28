from src import create_flask_app


if __name__ == '__main__':
    app = create_flask_app()
    app.run(ssl_context='adhoc', use_reloader=False)
