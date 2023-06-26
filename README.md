## Decorators Parser

### License
© 2023 Smartschool Inc. All rights reserved.

### Installation guide
1. Install Python 3.7 or newer from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Install PIP using [this guide](https://pip.pypa.io/en/stable/installation/)
3. Run `pip install decorator-parser` in your command line

### Decorators format
Decorator name can be any string that does not contain '@' character. If decorator
does not satisfy this requirement `InvalidDecoratorException` will be thrown.

#### Example:
```
@decorator(some nice value)
```

### Standard decorators
Decorators can be used in one of three ways:
```
@decorator(value)
```
or
```
@decorator()
Some very long and complicated value that would be hard to read if it were in parenthesis like the value above.
```
or
```
@decorator
Some very long and complicated value that would be hard to read if it were in parenthesis like the value above.
```

All of these create Python dictionary like this:
```python
{
    'decorator': 'value'
}
```

### @new decorator

Using @new decorator starts a new dictionary and adds it to the current list of dictionaries. In a single piece of text between two @new decorators (which correspond to a single Python dictionary) there can not be two decorators with the same name. Using a same name without an appropriate @new decorator will result in `DuplicateDecoratorException` being thrown.

#### Example:
task.txt:
```
@question()
Who is Lincoln?

@new
@question()
What is the purpose of the Bill of Rights?
```

run.py:
```python
from decorator_parser.parse import Parser
task_parser = Parser()
print(task_parser.parse_file('task.txt'))
```

result:
```python
[
    {
        'question': 'Who is Lincoln?'
    },
    {
        'question': 'What is the purpose of the Bill of Rights?'
    }
]
```
### Global decorators

In addition to standard decorators, decorators which name starts with `global-` are added to each dictionary while parsing a file. Dictionary key is the decorator's suffix after `global-` 

#### Example:
task.txt:
```
@global-topic(History)
@question()
Who is Lincoln?

@new
@question()
What is the purpose of the Bill of Rights?
```

run.py:
```python
from decorator_parser.parse import Parser
task_parser = Parser()
print(task_parser.parse_file('task.txt'))
```

result:
```python
[
    {
        'topic': 'History',
        'question': 'Who is Lincoln?'
    },
    {
        'topic': 'History',
        'question': 'What is the purpose of the Bill of Rights?'
    }
]
```

### Constraints

Decorators can use constraints on their values. If a decorator has value that does not match regular expression
provided, Parser will throw `InvalidValueException`. Parser class takes optional `constraints` argument in its constructor which
is a Python dictionary in a format shown below (if format of the given dictionary is invalid, `InvalidConstraintException` will be thrown):
```python
example = {
    'question': 
    {
        'regex': '([^@]+)',
        'description': 'any non-empty string without @'
    },
    'correct':
    {
        'regex': '([1-4])',
        'description': 'any number from 1 to 4'
    }
}
```


#### Example 1

task.txt:
```
@correct(11)
```

run.py:
```python
from decorator_parser.parse import Parser
task_parser = Parser(example)
print(task_parser.parse_file('task.txt'))
```

Will result in the following output:
```
errors.InvalidValueException: Line 1: 'correct' should be any number from 1 to 4 but is 11
```

#### Example 2
If we take Example 1 but change task.txt file to:
```
correct(1)
```

The output will be:
```python
[
    {
        'correct': '1'
    }
]
