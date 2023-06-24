import sys
from parse import Parser
from parse_task import TaskParser

task_parser = TaskParser(
    {
        'question': 
        {
            'regex': '([^@]+)',
            'description': 'any non-empty string without @'
        },
        'correct':
        {
            'regex': '([1-4])',
            'description': 'any number from 1 to 4'
        },
        'calculator':
        {
            'regex': '([0-1])',
            'description': '0 or 1'
        }
    }
)

print(task_parser.parse_file(sys.argv[1]))