class JSONExceptionHandler(Exception):
    status_code = 400
    message = "No JSON found"
    code = 6

    def __init__(self, message=None, status_code=None, payload=None): # pragma: no cover
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        if payload is not None:
            self.payload = payload

    def to_dict(self):
        return self.message


class ProductException(Exception):
    status_code = 400
    message = "Product not found"
    code = 2

    def __init__(self, prod, message=None, status_code=None):
        Exception.__init__(self)
        self.prod = prod
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return self.message + ' (' + str(self.prod) + ')'


class TradeException(ProductException):
    code = 2
    message = "Trade not found"

    def __init__(self, prod, message=None, status_code=None):
        ProductException.__init__(self,  prod, message, status_code)

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
        return self.message + ' (' + self.user + ')'


class UserNotPermission(UserException):
    code = 3
    message = "Not enough permissions"

    def __init__(self, user, message=None, status_code=None):
        UserException.__init__(self,  user, message, status_code)


class UserBanned(UserException):
    code = 7
    message = "User Banned"
    until_date = "Undefined"
    reason = "Ban reason"

    def __init__(self, user, message=None, until=None, reason=None, status_code=None):
        UserException.__init__(self,  user, message, status_code)
        if until is not None:
            self.until_date = str(until)
        if reason is not None:
            self.reason = str(reason)


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
