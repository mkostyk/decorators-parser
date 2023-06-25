## Decorators Parser

### License
© 2023 Smartschool Inc. All rights reserved.

### Standard decorators
Decorators can be used in one of two ways:
```
@decorator(value)
```
or
```
@decorator()
Some very long and complicated value that would be hard to read if it were in parenthesis like the value above.
```

Both of these create Python dictionary like this:
```python
{
    'decorator': 'value'
}
```

### @new decorator

Using @new decorator starts a new dictionary and adds it to the current list of dictionaries

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
from parse import Parser
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
from parse import Parser
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
from parse import Parser
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
