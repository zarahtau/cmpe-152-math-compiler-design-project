"""
===== LexicalAnalyzer.py =====
First phase of the compiler that converts a stream of characters from a source program
into a sequence of tokens.

The keywords to identify are:
[1] Identifiers
[2] Operators
[3] Terminators

Lexical Input:  Raw string typed by the user
Lexical Output: List of (TOKEN_TYPE, LEXEME) tuples

Example:
Input:
    int y = 4 + 3;

Output:
[
    ("TYPE", "int"),
    ("IDENT", "y"),
    ("ASSIGN", "="),
    ("NUMBER", "4"),
    ("OP", "+"),
    ("NUMBER", "3"),
    ("SEMICOLON", ";")
]
"""

import re

# ----------------------------------------------------------------------
# Token definitions (order matters!)
# ----------------------------------------------------------------------
_TOKEN_SPEC = [
    ("TYPE",      r"\b(?:int|double)\b"),   # Specific keywords must come first
    ("IDENT",     r"[A-Za-z][A-Za-z0-9]*"), # Variable names (alphabetic only)
    ("NUMBER",    r"(?:\d+\.\d+|\d+)"),     # Integer or float literals
    ("ASSIGN",    r"="),                    # Assignment operator
    ("OP",        r"[+\-*/]"),              # Arithmetic operators
    ("SEMICOLON", r";"),                    # Statement terminator
    ("WS",        r"\s+"),                  # Whitespace (ignored)
]

# Build a single master regex
_MASTER = re.compile("|".join(f"(?P<{k}>{pat})" for k, pat in _TOKEN_SPEC))

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _err(msg):
    print(f"Lexical error: {msg}")

# ----------------------------------------------------------------------
# Lexical analyzer function
# ----------------------------------------------------------------------
def test_lexical(user_input: str):
    print("[LEXICAL ANALYSIS]")

    if not isinstance(user_input, str):
        _err("Input must be a string.")
        return []
    if not user_input.strip():
        _err("Empty input.")
        return []

    tokens = []
    pos = 0
    n = len(user_input)

    while pos < n:
        match = _MASTER.match(user_input, pos)
        if not match:
            snippet = user_input[pos:pos+10]
            _err(f"Invalid token starting at position {pos}: {snippet!r}")
            return []
        kind = match.lastgroup
        lexeme = match.group()
        pos = match.end()

        if kind != "WS":
            tokens.append((kind, lexeme))

    for kind, lexeme in tokens:
        matches = [k for k, pat in _TOKEN_SPEC if re.fullmatch(pat, lexeme)]
        if kind not in matches:
            _err(f"Token {lexeme!r} misclassified as {kind}, possible match: {matches}")

    # Print and return
    for token in tokens:
        print(token)
    print()
    return tokens

# ----------------------------------------------------------------------
# Unit Test Suite
# ----------------------------------------------------------------------
def _test_suite():
    tests = {
        "int y = 4 + 3;": [
            ("TYPE", "int"), ("IDENT", "y"), ("ASSIGN", "="),
            ("NUMBER", "4"), ("OP", "+"), ("NUMBER", "3"), ("SEMICOLON", ";")
        ],
        "double a = 7.5;": [
            ("TYPE", "double"), ("IDENT", "a"), ("ASSIGN", "="),
            ("NUMBER", "7.5"), ("SEMICOLON", ";")
        ],
        "x = 10;": [
            ("IDENT", "x"), ("ASSIGN", "="), ("NUMBER", "10"), ("SEMICOLON", ";")
        ],
    }

    for src, expected in tests.items():
        print(f"--- Testing: {src!r} ---")
        result = test_lexical(src)
        if result == expected:
            print("PASS\n")
        else:
            print("FAIL\nExpected:", expected, "\nGot:", result, "\n")

# ----------------------------------------------------------------------
# Run tests if executed directly
# ----------------------------------------------------------------------
if __name__ == "__main__":
    _test_suite()
