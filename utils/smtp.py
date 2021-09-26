def init_smtp(app):
    """
    This function will register SMTP object to flask app context for further using in service views
    :param app: initialized flask app
    :return: None
    """

    app.smtp = SMTP()


# This protocol sending emails to user.
class SMTP:
    def __init__(self):
        pass
