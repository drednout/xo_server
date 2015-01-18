import os
import inspect

ERROR_NO_REQUIRED_ARG = 1
ERROR_BAD_LOGIN_OR_PASSWORD = 2
ERROR_PASSWORD_NOT_MATCH = 3
ERROR_PLAYER_IS_EXISTS = 4
ERROR_NO_PASSWORD_HASH = 5
ERROR_INVALID_PLAYER_EMAIL = 6
ERROR_INVALID_SID = 7
ERROR_INVALID_PLAYER_ID = 8
ERROR_INVALID_MOVE = 9

ERROR_INTERNAL_SERVER_ERROR = 500


DEFAULT_ERROR_MSG = "Internal server error"
ERROR_MESSAGES = {
    ERROR_NO_REQUIRED_ARG: "You need to specify required argument",
    ERROR_INTERNAL_SERVER_ERROR: DEFAULT_ERROR_MSG,
    ERROR_BAD_LOGIN_OR_PASSWORD: "Bad login or password",
}

def err2msg(err_code):
    if ERROR_MESSAGES.has_key(err_code):
        return ERROR_MESSAGES[err_code]
    return DEFAULT_ERROR_MSG


def create_error(err_code):
    err_msg = err2msg(err_code)
    resp = {}
    resp["err_code"] = err_code
    resp["err_msg"] = err_msg
    return resp


def is_error(msg):
    if ("err_code" in msg and
        "err_msg" in msg):
        return True

    return False

def get_frame_info_without_leak(back_counter=1):
    f = inspect.currentframe()
    try:
        if f is not None:
            for i in xrange(back_counter):
                f = f.f_back
            exc_lineno = f.f_lineno
            co = f.f_code
            exc_funcname = co.co_name
            #only last 3 path entries are intresting for us
            exc_filename = os.path.sep.join(co.co_filename.split(os.path.sep)[-3:])
    finally:
        del f

    return exc_lineno, exc_funcname, exc_filename


class EInternalError(Exception):
    def __init__(self, error_id, **kwargs):
        self.error_id = error_id
        self.error_background = kwargs
        self.error_to_client = None
        if 'to_client' in kwargs:
            self.error_to_client = kwargs.pop('to_client')
        self.error_message = err2msg(self.error_id)
        self.exc_lineno, self.exc_funcname, self.exc_filename = get_frame_info_without_leak(back_counter=2)
        if ERROR_MESSAGES.has_key(error_id):
            self.error_message = ERROR_MESSAGES[error_id]
            

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        output_msg =  "Error %d -> %s. " % (self.error_id, self.error_message)
        output_msg += "Where? [%s: %s +%s] " % (str(self.exc_funcname), str(self.exc_filename), str(self.exc_lineno))
        output_msg += "Details: "
        for k, v in  self.error_background.iteritems():
            value_as_str = str(v)
            if len(value_as_str) > 256:
                value_as_str = value_as_str[:256]
            output_msg += "[%s: %s] " % (str(k), value_as_str)
        return output_msg


    def get_client_error(self):
        return self.error_message

def create_response(err):
    if isinstance(err, EInternalError):
        return {'errorCode': err.error_id, 'errorMessage': err.error_message}
    else:
        return {'errorCode': ERROR_INTERNAL_SERVER_ERROR, 'errorMessage': DEFAULT_ERROR_MSG}
