# Author: Michał Kostyk for Smartschool Inc.
# Date: 2023
# Version: 1.0.4

from errors import *
from utils import *
import re


class Parser:
    def __init__(self, constraints={}):
        for key in constraints:
            if not 'regex' in constraints[key] or not 'description' in constraints[key]:
                raise InvalidConstraintException(f"Invalid constraint for '{key}'")

        self.constraints = constraints
        pass
        

    # Parse @global decorators
    def parse_global(self, data):
        global_decorators = re.findall(r'(@global\-[^\n]*)', data)
        if len(global_decorators) == 0:
            return data, {}
        
        # Removing decorators from data
        for gd in global_decorators:
            data = data.replace(gd, '')
        
        gd_text = '\n'.join(global_decorators)
        gd_result = self.create_result(gd_text, {})

        return data, gd_result


    # Splits file by @new decorator
    def split_by_new(self, data):
        return data.split('@new')


    # Removes decorator and its value from data
    def remove_decorator(self, data):
        splitted = data.split('@')
        # This means that splitted looks like ['', decorator] right now, so it
        # is the last decorator, and after deletion we want it to be ""
        if len(splitted) <= 2:
            return ""

        data = '@' + '@'.join(data.split('@')[2:])

        return data


    # Handles a single decorator.
    def handle_decorator(self, data, result):       
        # Look for a decorator
        decorator = re.search(r'(@[^\n]*$)', data, re.MULTILINE)
        if decorator is None:
            raise DecoratorNotFoundException("No more decorators found")
        decorator = decorator.group(0)

        # Check if decorator is valid
        if re.search(r'(@[^\n]*@[^\n]*$)', decorator, re.MULTILINE) is not None:
            raise InvalidDecoratorException(self.original_data, decorator, "Invalid decorator")
        
        is_global = re.search(r'(@global\-[^\n]*)', decorator) is not None       
        name = decorator.split('(')[0].split('@')[1]
        if is_global:
            # Removing global- prefix from name
            name = name.replace('global-', '')

        decor_with_val = decorator # For error messages
        value = ""

        # Value can be put in brackets or after decorator
        try:
            value = decorator.split('(')[1].split(')')[0].strip()
        except IndexError:
            pass

        if value == "":
            value = data.split(decorator)[1].split('@')[0].strip()
            decor_with_val += value

        if name in result:
            raise DuplicateDecoratorException(f"Duplicate decorator '{name}'")

        if name in self.constraints:
            description = self.constraints[name]['description']

            # Checking constraint match
            if not re.fullmatch(self.constraints[name]['regex'], value):
                raise InvalidValueException(self.original_data, decor_with_val, f"'{name}' should be {description} but is {value}")
            
        result[name] = value

        return result


    # Handles all decorators in a single @new object
    def create_result(self, data, global_dec):
        result = global_dec.copy()
        while True:
            try:
                # Handle decorator and remove it from data
                result = self.handle_decorator(data, result)
            except DecoratorNotFoundException:
                # No more decorators found
                break
            
            data = self.remove_decorator(data)
        return result


    # Main function for parsing file
    def parse_file(self, path):
        with open(path, 'r') as f:
            data = f.read()

        # Save original data for error line messages
        self.original_data = data

        # Parse global decorators
        data, global_dec = self.parse_global(data)

        # Split file by @new decorator
        data = self.split_by_new(data)

        results_list = []
        for d in data:
            # Handle a single @new object
            results_list.append(self.create_result(d, global_dec))

        return results_list