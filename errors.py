from enum import Enum
from psychopy import core


class ErrorType(Enum):
    OK = (1, "Ok.")
    USER_TERMINATED = (2, "Terminated by user.")
    UNKNOWN = (99, "Unknown error occured.")
    
    def __init__(self, code, message):
        self.code = code
        self.message = message
    
    def print(self):
         print(f"Error Code: {self.code}, Message: {self.message}")

def handle_error(error):
    if error == ErrorType.USER_TERMINATED:
        error.print()
        core.quit()
        return
    else:
        error.print()
        return 