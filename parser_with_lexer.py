'''
items = item | item, items
item = key ':' value
key = '"' [a-zA-Z0-9] "
value = key

"hell": "323"
"he": "she", "hi": "her"

'''
from lexer import Lexer, Token
class Item:
    def __init__(self, key, value, item_type) -> None:
        self.key = key
        self.value = value
        self.type = item_type
class Parser:
    def __init__(self):
        pass
    def parse(self, s):
        lexer = Lexer()
        lexemes = lexer.lexers(s)
        if len(lexemes) < 2:
            Exception('Ill format json.')
        item, _ =  self.parse_value(lexemes)
        return item.value
    def parse_value(self, lexemes: list[Token]):
        if len(lexemes) == 0:
            return Item('string', '', 'string')
        if lexemes[0].lexeme == '{':
            return self.parse_object(lexemes)
        if lexemes[0].lexeme == '[':
            return self.parse_array(lexemes)
        if lexemes[0].lexeme == '"':
            item, lexemes = self.get_string(lexemes)
            return item, lexemes

        def is_value(s: Token):
            return s.type == 'string' or s.type == 'integer' or s.type == 'boolean'
        if not is_value(lexemes[0]):
            raise Exception("value is not support")
        if lexemes[0].type == 'integer':
            return Item('value', int(lexemes[0].lexeme), 'integer'), lexemes[1:]
        if lexemes[0].lexeme in ['True', 'False']:
            return Item('value', lexemes[0].lexeme == 'True', 'boolean'), lexemes[1:]
        raise Exception('Not supported yet!')
    def get_string(self, lexemes):
        if len(lexemes) < 3:
            raise Exception('Not a string')
        return Item('string', lexemes[1].lexeme, 'string'), lexemes[3:]
    def parse_object(self, lexemes):
            _, lexemes = self.get_left_bracket(lexemes)
            items = []
            if lexemes[0].type != '}':
                items, lexemes = self.parse_items(lexemes)
            _, lexemes = self.get_right_bracket(lexemes)

            res = {}
            for i in items:
                res[i.key] = i.value
            return Item('object', res, 'object'), lexemes
    def parse_array(self, lexemes):
            _, lexemes = self.get_left_square_bracket(lexemes)
            items = []
            item, lexemes = self.parse_value(lexemes)
            items.append(item.value)
            while lexemes[0].lexeme != ']' and len(lexemes) > 1:
                item, lexemes = self.parse_value(lexemes[1:])
                items.append(item.value)

            _, lexemes = self.get_right_square_bracket(lexemes)
            return Item('array', items, 'array'), lexemes
        
    def parse_items(self, lexemes: list[Token]):
        items = []
        if len(lexemes) == 0:
            return items
        item, lexemes = self.get_item(lexemes)
        if len(lexemes) != 0 and lexemes[0].type == ',':
            items, lexemes = self.parse_items(lexemes[1:])
        return [item] + items, lexemes

    def get_item(self, s:list[Token]):
        if s== "":
            raise Exception("empty string is not a item")
        key, s = self.get_string(s)
        _, s = self.get_colon(s)
        value, s = self.parse_value(s)
        return Item(key.value, value.value, 'item'), s
    def get_right_square_bracket(self, s):
        if len(s) == 0 or s[0].type != ']':
            raise Exception("Right square bracket expected.")
        return ']', s[1:]
    def get_left_square_bracket(self, s):
        if len(s) == 0 or s[0].type != '[':
            raise Exception("Left square bracket expected.")
        return '{', s[1:]
    def get_right_bracket(self, s):
        if len(s) == 0 or s[0].type != '}':
            raise Exception("Right bracket expected.")
        return '}', s[1:]
    def get_left_bracket(self, s):
        if len(s) == 0 or s[0].type != '{':
            raise Exception("Left bracket expected.")
        return '{', s[1:]
    def get_colon(self, s: list[Token]):
        '''
        Return the string after colon
        '''
        if len(s) == 0:
            raise Exception('colon is expected.')
        if s[0].type != ':':
            raise Exception('colon is expected.')
        return ':', s[1:]

    if __name__ == '__main__':
        #print(parse_items('"hell": "323"'))
        pass

