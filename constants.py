token_patterns = [
    ("Open brace", r'^{'),
    ("Close brace", r'^}'),
    ("Open parenthesis", r'^\('),
    ("Close parenthesis", r'^\)'),
    ("Semicolon", r'^;'),
    ("Int keyword", r"^int"),
    ("Return keyword", r"^return"),
    ("Identifier", r"^[a-zA-Z][a-zA-Z0-9]*"),
    ("Integer literal", r'^[0-9]+'),
    ("white space", r"^[ \t\r\n]"),
    ("Negation", r"^-"),
    ('Bitwise complement', r'~'),
    ('Logical negation', r'^!')
]

unary_operators = ["Negation", "Bitwise complement", "Logical negation"]
