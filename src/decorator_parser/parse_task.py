#from decorator_parser.parse import Parser
from parse import Parser

class TaskParser(Parser):
    def create_result(self, data, global_dec):
        result = super().create_result(data, global_dec)
        if 'answers' in result:
            result['answers'] = result['answers'].split('\n')
        
        return result