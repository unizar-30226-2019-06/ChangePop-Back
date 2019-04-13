class JSONExceptionHandler(Exception):
    status_code = 400
    message = "No JSON found"
    code = 6

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        if payload is not None:
            self.payload = payload

    def to_dict(self):
        return self.message


class UserException(Exception):
    status_code = 400
    message = "User not found"
    code = 2

    def __init__(self, user, message=None, status_code=None):
        Exception.__init__(self)
        self.user = user
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return self.message + '(' + self.user + ')'


class UserNotPermission(UserException):
    code = 3
    message = "Not enough permissions"

    def __init__(self, user, message=None, status_code=None):
        UserException.__init__(self,  user, message, status_code)


class UserPassException(UserException):
    code = 3
    message = "Wrong Password"

    def __init__(self, user, message=None, status_code=None):
        UserException.__init__(self,  user, message, status_code)


class NotLoggedIn(Exception):
    status_code = 400
    message = "Not logged in"
    code = 5

    @staticmethod
    def not_auth_handler():
        raise NotLoggedIn()

    def __init__(self, user=None, message=None, status_code=None):
        Exception.__init__(self)
        self.user = user
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return self.message
