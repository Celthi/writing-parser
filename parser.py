'''
items = item | item, items
item = key ':' value
key = '"' [a-zA-Z0-9] "
value = key

"hell": "323"
"he": "she", "hi": "her"

'''
def parse_items(s):
    items = []
    if s == "":
        return items
    s = skip_whitespace(s)
    if s[0] != '"':
        raise Exception("not begin with quotes")
    item, s = parse_item(s)
    if s != "":
        if s[0] == ',':
            items = parse_items(s[1:])
        else:
            raise Exception("str not end correctly.")
    return [item] + items
def parse_item(s):
    if s== "":
        raise Exception("empty string is not a item")

    key, s = get_key(s)
    _, s = get_colon(s)
    value, s = get_value(s)
    return {key: value}, s

def get_colon(s: str):
    '''
    Return the string after colon
    '''
    s = skip_whitespace(s)
    i = s.find(':')
    return ':', s[i+1:]
def skip_whitespace(s):
    i = 0
    while i < len(s):
        if s[i] == ' ':
            i += 1
        else:
            break
    return s[i:]
def get_key(s):
    '''
    Return (key, left string)
    '''
    if s[0] != '"':
        raise Exception("key should start with quote")
    idx = s.find('"', 1)
    
    return s[1:idx], s[idx+1:]

def get_value(s: str):
    s = skip_whitespace(s)
    if s[0] != '"':
        raise Exception("value should start with quote")
    i = s.find('"', 1)
    return s[1: i], s[i+1:] 
if __name__ == '__main__':
    print(parse_items('"hell": "323"'))

