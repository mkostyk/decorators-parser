# Author: Michał Kostyk for Smartschool Inc.
# Date: 2023
# Version: 1.0.0
# Description: Custom errors for the project.

from utils import FAIL, ENDC, BOLD

# TODO: this is not perfect
def line_number(data, line):
    matches = data.split(line)
    return len(matches[0].split('\n'))


# Exception class that adds coloring to the message
class FailException(Exception):
    def __init__(self, message):
        self.message = FAIL + message + ENDC
        super().__init__(self.message)


# Exception class that adds line number to the message
class ExceptionWithLine(FailException):
    def __init__(self, data, value, message):
        self.line = line_number(data, value)
        self.message = BOLD + FAIL + f"Line {self.line}: " + message
        super().__init__(self.message)


class DecoratorNotFoundException(FailException):
    ...
    pass


class InvalidConstraintException(FailException):
    ...
    pass


class InvalidDecoratorException(ExceptionWithLine):
    ...
    pass


class InvalidValueException(ExceptionWithLine):
    ...
    pass