import json
from pygments.lexer import RegexLexer
from pygments.token import *

class DbufLexer(RegexLexer):
    name = "DependoBuf"
    aliases = ["dbuf"]
    filenames = ["*.dbuf"]

    tokens = {
        'root': [
            # Blocks using for documentation only
            (r'\[[^\]]*\]', String), 
            (r'\!\{', String), 
            (r'\}\!', String), 

            # Space
            (r'\s+', Whitespace),
            
            # Keyword type declaration
            (r'\b(message)\b', Keyword.Declaration),
            (r'\b(enum)\b', Keyword.Declaration),
            (r'\b(use)\b', Keyword.Declaration),
            (r'\b(as)\b', Keyword.Declaration),

            # Boolean constants
            (r'\b(true)\b', Keyword.Constant),
            (r'\b(false)\b', Keyword.Constant),

            # Type name
            (r'\b([A-Z]\w*)\b', Name.Class),

            # Var name (also a.b.c)
            (r'\b([a-z]\w*(?:\.[a-z]\w*)*)\b', Name.Variable),
            
            # Numeric literals
            (r'\b(\d+\.\d+)\b', Number.Float),
            (r'\b(\d+u)\b', Number.Integer), 
            (r'\b(\d+)\b', Number.Integer),

            # String literal
            (r'"', String.Double, 'string'),

            # Single line comment
            (r"//.*", Comment.Single),

            # Multiline comment
            (r"/\*", Comment.Multiline, 'comment'),
    
            # Empty pattern
            (r'\*(?=\s*,|\s*=>|\s*})', Keyword.Constant),

            # Empty pattern followed by comment, only for docs:
            # * followed by comments can be only if * is pattern match
            (r'\*(?=\s*/)', Keyword.Constant),

            # Operators
            (r'=>', Operator),
            (r'[+\-*/&|!]', Operator),
            
            # Punctuation
            (r'[{}().,;:]', Punctuation),
        ],
        
        'string': [
            (r'\\.', String.Escape),
            (r'"', String.Double, '#pop'),
            (r'[^\\"]+', String.Double),
        ],

        'comment': [
            (r'\*/', Comment.Multiline, "#pop"),
            (r'[^*]+', Comment.Multiline),
        ],
    }

