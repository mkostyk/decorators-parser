## Decorators Parser

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
		'topic': 'History'
		'question': 'What is the purpose of the Bill of Rights?'
	}
]
```
