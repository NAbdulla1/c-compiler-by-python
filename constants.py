token_patterns = [
    ("Open brace", r'^{\s*'),
    ("Close brace", r'^}\s*'),
    ("Open parenthesis", r'^\(\s*'),
    ("Close parenthesis", r'^\)\s*'),
    ("Semicolon", r'^;\s*'),
    ("Int keyword", r"^int\s+"),
    ("Return keyword", r"^return\s+"),
    ("Identifier", r"^[a-zA-Z]\w*\s*"),
    ("Integer literal", r'^[0-9]+\s*'),
    ("Negation", r"^-\s*"),
    ('Bitwise complement', r'~\s*'),
    ('Logical negation', r'^!\s*'),
    ("Addition", r"^[+]\s*"),
    ("Multiplication", r"^[*]\s*"),
    ("Division", r"^[/]\s*"),
    ("white space", r"^\s+")
]

unary_operators = ["Negation", "Bitwise complement", "Logical negation"]
binary_operators = ["Addition", "Multiplication", "Division"]
