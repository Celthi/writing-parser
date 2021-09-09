from parser_with_lexer import Parser
import unittest
from parser import parse_items
from lexer import Lexer, Token


class TestParser(unittest.TestCase):
    def test_parser_item(self):
        self.assertListEqual([{"hell": "323"}], parse_items('"hell": "323"'))
        self.assertListEqual(
            [{"hell": "323"}], parse_items('"hell":     "323"'))
        self.assertListEqual(
            [{"hell": "323"}], parse_items('"hell"    :     "323"'))
        self.assertListEqual([{"hell": "323"}, {"she": "good"}], parse_items(
            '"hell":     "323", "she": "good"'))
        self.assertListEqual([{"hell": "323"}, {"she": "good"}], parse_items(
            '    "hell":     "323",   "she"   : "good"'))


def AssertTokensEqual(case: unittest.TestCase, left: list, right: list):
    for l, r in zip(left, right):
        case.assertEqual(l.lexeme, r.lexeme)
        case.assertEqual(l.type, r.type)


class TestLexer(unittest.TestCase):
    def test_lexer(self):
        lexer = Lexer()
        self.assertEqual([], lexer.lexers(''))
        AssertTokensEqual(self, [Token('{', '{')], lexer.lexers('{'))
        AssertTokensEqual(self, [Token('}', '}')], lexer.lexers('}'))
        AssertTokensEqual(self, [Token('[', '[')], lexer.lexers('['))
        AssertTokensEqual(self, [Token('{', '{')], lexer.lexers('{'))
        AssertTokensEqual(self, [Token('{', '{')], lexer.lexers('{'))
        AssertTokensEqual(self, [Token('{', '{'),
                                 Token('"', 'quote'),
                                 Token('key', 'string'),
                                 Token('"', 'quote'),
                                 Token(':', ':'),
                                 Token('"', 'quote'),
                                 Token('value', 'string'),
                                 Token('"', 'quote'),
                                 Token('}', '}')], lexer.lexers('{ "key": "value"} '))
        AssertTokensEqual(self, [Token('{', '{'),
                                 Token('"', 'quote'),
                                 Token('key', 'string'),
                                 Token('"', 'quote'),
                                 Token(':', ':'),
                                 Token('"', 'quote'),
                                 Token('value', 'string'),
                                 Token('"', 'quote'),
                                 Token('}', '}'),
                                 Token(',', ',')], lexer.lexers('{ "key": "value"}, '))
        AssertTokensEqual(self, [Token('{', '{'),
                                 Token('"', 'quote'),
                                 Token('key', 'string'),
                                 Token('"', 'quote'),
                                 Token(':', ':'),
                                 Token('"', 'quote'),
                                 Token('value', 'string'),
                                 Token('"', 'quote'),
                                 Token('}', '}'),
                                 Token(',', ',')], lexer.lexers('{  "key"  : "value"}  , '))
        AssertTokensEqual(self, [Token('{', '{')], lexer.lexers('{'))


class TestParserLexer(unittest.TestCase):
    def test_parse(self):
        parser = Parser()
        self.assertDictEqual(
            {"key": "value"}, parser.parse('{  "key"  : "value"}'))
        self.assertDictEqual({"key": 234}, parser.parse('{  "key"  : 234 }'))
        self.assertDictEqual({}, parser.parse('{}'))
        self.assertDictEqual({"key": 234, "k2": "value"},
                             parser.parse('{  "key"  : 234, "k2": "value" }'))
        self.assertDictEqual({"key": 234, "k2": "value", "k3": "v3"}, parser.parse(
            '{  "key"  : 234, "k2": "value" , "k3": "v3"}'))
        self.assertDictEqual({"key": 234, "k2": "value", "k3": "v3",  "k4": {"ik1": "iv"}}, parser.parse(
            '{  "key"  : 234, "k2": "value" , "k3": "v3", "k4": {"ik1": "iv"} }'))
        self.assertDictEqual({"key": 234, "k2": "value", "k3": "v3",  "k4": {"ik1": "iv", "ik2": 678}}, parser.parse(
            '{  "key"  : 234, "k2": "value" , "k3": "v3", "k4": {"ik1": "iv",  "ik2": 678}} }'))

    def test_parse_newline(self):
        parser = Parser()
        self.assertDictEqual({"key": 234, "k2": "value"}, parser.parse('''{  "key"  : 234,
         "k2": "value" }'''))
        self.assertDictEqual({"key": 234, "k2": "value"}, parser.parse('''{
        "key"  : 234,
         "k2": "value" }'''))

    def test_parse_boolean(self):
        parser = Parser()
        self.assertDictEqual({"key": True}, parser.parse('{"key": True }'))
        self.assertDictEqual({"key": True}, parser.parse('{"key": True}'))

    def test_parse_array(self):
        parser = Parser()
        self.assertDictEqual({"key": [{"k2": "v2"}]}, parser.parse(
            '{"key": [ {"k2": "v2"} ] }'))
        self.assertDictEqual({"key": [{"k2": "v2"}, 256]}, parser.parse(
            '{"key": [ {"k2": "v2"}, 256 ] }'))
        self.assertDictEqual({"key": [{"k2": "v2"}, 256, 234]}, parser.parse(
            '{"key": [ {"k2": "v2"}, 256, 234 ] }'))
        self.assertDictEqual({"key": [{"k2": "v2"}, 256, [234]]}, parser.parse(
            '{"key": [ {"k2": "v2"}, 256, [234] ] }'))
        self.assertDictEqual({"key": [{"k2": "v2"}, 256, [True]]}, parser.parse(
            '{"key": [ {"k2": "v2"}, 256, [True] ] }'))

    def test_parse_value(self):
        parser = Parser()
        self.assertDictEqual({"key": [{"k2": "v2"}]}, parser.parse(
            '{"key": [ {"k2": "v2"} ] }'))
        self.assertDictEqual({"key": [{"k2": "v2"}, 256]}, parser.parse(
            '{"key": [ {"k2": "v2"}, 256 ] }'))
        self.assertDictEqual({"key": [{"k2": "v2"}, 256, 234]}, parser.parse(
            '{"key": [ {"k2": "v2"}, 256, 234 ] }'))
        self.assertDictEqual({"key": [{"k2": "v2"}, 256, [234]]}, parser.parse(
            '{"key": [ {"k2": "v2"}, 256, [234] ] }'))
        self.assertDictEqual({"key": [{"k2": "v2"}, 256, [True, {"hi": "world"}]]}, parser.parse(
            '{"key": [ {"k2": "v2"}, 256, [True, {"hi": "world"}] ] }'))
        self.assertDictEqual({
            "name": "good",
            "books": ["C++", "Rust", 234],
            "great": True,
            "year": 2200
        }, parser.parse('''{
            "name": "good",
            "books": [ "C++", "Rust", 234],
            "great": True,
            "year": 2200
            }'''))

    def test_fail_cases(self):
        parser = Parser()
        self.assertRaises(Exception, parser.parse, '')


if __name__ == '__main__':
    unittest.main()
