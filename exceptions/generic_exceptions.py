from pydantic import BaseModel


class CustomError(BaseModel):
    error_code: int
    error_message: str


class CustomException(Exception):
    def __init__(self, error_code: int, error_message: str, response_code: int):
        self.error_code = error_code
        self.error_message = error_message
        self.response_code = response_code


USER_EXISTS_EXCEPTION_CODE = 1001
USER_DOES_NOT_EXISTS_EXCEPTION_CODE = 1002
USER_WRONG_CREDENTIALS_EXCEPTION_CODE = 1003
USER_EXPIRED_TOKEN = 1004
USER_INVALID_TOKEN_TYPE = 1004
USER_INVALID_VERIFICATION_CODE = 1005
USER_ALREADY_VERIFIED = 1006


def get_user_exceptions():
    return {
        "USER_EXISTS_EXCEPTION_CODE": USER_EXISTS_EXCEPTION_CODE,
        "USER_DOES_NOT_EXISTS_EXCEPTION_CODE": USER_DOES_NOT_EXISTS_EXCEPTION_CODE,
        "USER_WRONG_CREDENTIALS_EXCEPTION_CODE": USER_WRONG_CREDENTIALS_EXCEPTION_CODE,
        "USER_EXPIRED_TOKEN": USER_EXPIRED_TOKEN,
        "USER_INVALID_TOKEN_TYPE": USER_INVALID_TOKEN_TYPE,
        "USER_INVALID_VERIFICATION_CODE": USER_INVALID_VERIFICATION_CODE,
        "USER_ALREADY_VERIFIED": USER_ALREADY_VERIFIED,
    }
