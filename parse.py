# Author: Michał Kostyk for Smartschool Inc.
# Date: 2023
# Version: 1.0.0

from errors import *
from utils import *

# Splits file by @new decorator
def split_by_new(data):
    return data.split('@new')


# Removes decorator and its value from data
def remove_decorator(data):
    splitted = data.split('@')
    if len(splitted) < 2:
        return ""

    data = '@' + '@'.join(data.split('@')[2:])

    return data


# Handles a single decorator.
def handle_decorator(data, result):
    data = data.split('@')[1:]
    if len(data) < 2:
        raise DecoratorNotFoundException("No decorator found")
    
    data = data[0]
    try:
        decorator = data.split('(')[0]
    except IndexError:
        raise InvalidDecoratorException("Lacking opening parenthesis in decorator")
    
    value = None
    # There are two options how to put value: @decorator(value) or @decorator() value
    try:
        value = data.split('(')[1].split(')')[0]
    except IndexError:
        raise InvalidDecoratorException("Lacking closing parenthesis in decorator")
    
    if value == "":
        try:
            value = data.split(')')[1].strip()
        except IndexError:
            raise InvalidDecoratorException("Lacking value in decorator")

    result[decorator] = value

    return result


# Splits single data by decorators
def split_by_decorators(data):
    result = {}
    while True:
        try:
            # Handle decorator and remove it from data
            result = handle_decorator(data, result)
        except DecoratorNotFoundException:
            # No more decorators found
            break
        except InvalidDecoratorException:
            print_err("Invalid decorator found, skipping")
        
        data = remove_decorator(data)
    return result


# Main function for parsing file
def parse_file(path):
    with open(path, 'r') as f:
        data = f.read()

    # Split file by @new decorator
    data = split_by_new(data)

    results_list = []
    for d in data:
        # Split single data by decorators
        results_list.append(split_by_decorators(d))

    return results_list