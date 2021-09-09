'''
A lexer to tokenize the stream.

Tokenize the stream is important. Because when we build the AST, we don't want to tokenize the stream. It is tedious and building the AST, it is just building the AST, do one thing in a function.


'''

'''
token type:
string, enclosed by double quote
[
]
,
:
{

}
integer

'''
class Token:
    def __init__(self, lexeme, token_type) -> None:
        self.lexeme = lexeme
        self.type = token_type

class Lexer:
    def __init__(self) -> None:
        
        pass
    def add_token(self, tokens, s, start, end):
        if start == end:
            return
        tokens.append(Token(s[start:end], 'string'))

    def lexers(self, s: str) -> list[Token]:
        '''Return a list of lexemes
        '''

        res = []
        i = 0
        in_quote = False
        start = 0
        while i < len(s):
            if s[i] == '"':
                if in_quote:
                    lexeme = Token(s[start: i], 'string')
                    res.append(lexeme)
                    i += 1
                    start = i
                    in_quote = not in_quote
                    lexeme = Token('"', 'quote')
                    res.append(lexeme)
                    continue
                else:
                    in_quote = not in_quote
                    lexeme = Token('"', 'quote')
                    res.append(lexeme)
                    i += 1
                    start = i 
                    continue

            if in_quote:
                i += 1
                continue
            if s[i].isspace():
                    if i - start != 1:
                        lex = s[start:i] 
                        lexeme = Token(lex, 'unknown lexeme')
                        if lex in ['True', 'False']:
                            lexeme = Token(lex, 'boolean')
                            res.append(lexeme)
                        i += 1
                        start = i
                        continue
                    i +=1
                    start = i
                    continue
            if s[i] == '[':
                lexeme = Token('[', '[')
                res.append(lexeme)
                i += 1
                start = i
                continue
            if s[i] == ']':
                self.add_token(res, s, start, i)
                lexeme = Token(']', ']')
                res.append(lexeme)
                i +=1
                start = i
                continue
            if s[i] == '{':
                lexeme = Token('{', '{')
                res.append(lexeme)
                i += 1
                start = i
                continue
            if s[i] == '}':
                self.add_token(res, s, start, i)

                lexeme = Token('}', '}')
                res.append(lexeme)
                i += 1
                start = i
                continue
            if s[i] == ',':
                self.add_token(res, s, start, i)
                lexeme = Token(',', ',')
                res.append(lexeme)
                i += 1
                start = i
                continue
            if s[i] == ':':
                lexeme = Token(':', ':')
                res.append(lexeme)
                i += 1
                start = i
                continue
            if s[i].isdigit():
                start = i
                while s[i].isdigit():
                    i += 1
                lexeme = Token(s[start:i], 'integer')
                res.append(lexeme)
                start = i
                continue
            i += 1
        return res
            


            
            


        