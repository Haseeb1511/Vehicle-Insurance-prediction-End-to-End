import sys
import logging


def error_message_detail(error: Exception) -> str:
    # Extract traceback details
    _, _, exc_tb = sys.exc_info()

    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
    else:
        file_name = "Unknown"
        line_number = "Unknown"

    # Create a formatted error message
    error_message = (f"Error occurred in script: [{file_name}] at line no [{line_number}]: {str(error)}")
    
    logging.error(error_message)
    return error_message


class MyException(Exception):
    def __init__(self, original_exception: Exception):
        # Generate the detailed message
        self.error_message = error_message_detail(original_exception)
        # Initialize the base Exception class
        super().__init__(self.error_message)

    def __str__(self) -> str:
        return self.error_message
