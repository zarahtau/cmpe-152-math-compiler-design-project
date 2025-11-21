"""
 ===== LexicalAnalyzer.py =====
First pahse of the compiler that converts a stream of characters from a source porgram
into a sequence of tokens.

The keywords to identify are:
[1] Identifiers
[2] Operators
[3] Terminators
https://www.geeksforgeeks.org/compiler-design/introduction-of-lexical-analysis/
https://medium.com/@mitchhuang777/introduction-to-lexical-analysis-what-it-is-and-how-it-works-b25c52113405

The requirements for our LexicalAnalyzer is one that parses the input string
from the user and classifies the each of the tokens in the user input

Lexical Input: Raw string typed by the user:
Lexical Return: A python list of tokens which is to be passed to the sytax analyzer

Print and RETURN if pass:
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

"""
def test_lexical(user_input):
    print("Testing Lexical")
    
    return []
"""
# Validates the entire token stream and its exact order.
# Expected: TYPE IDENT ASSIGN NUMBER OP NUMBER SEMICOLON

import re

# Build a single master regex. Order matters (TYPE before IDENT).
_TOKEN_SPEC = [
    ("TYPE",      r"\b(?:int|double)\b"),  # only these two are valid types
    ("IDENT",     r"[A-Za-z]+"),           # alpha-only variable name per requirement
    ("NUMBER",    r"(?:\d+\.\d+|\d+)"),    # float or int literal
    ("ASSIGN",    r"="),
    ("OP",        r"[+\-*/]"),
    ("SEMICOLON", r";"),
    ("WS",        r"\s+"),                 # ignored
]

_MASTER = re.compile("|".join(f"(?P<{k}>{pat})" for k, pat in _TOKEN_SPEC))
_ALLOWED_KINDS = {"TYPE", "IDENT", "NUMBER", "ASSIGN", "OP", "SEMICOLON", "WS"}
_EXPECTED_SEQUENCE = ["TYPE", "IDENT", "ASSIGN", "NUMBER", "OP", "NUMBER", "SEMICOLON"]
_VALID_TYPES = {"int", "double"}
_VALID_OPS = {"+", "-", "*", "/"}


def _err(msg):
    print(f"Lexical error: {msg}")


def test_lexical(user_input: str):
    print("[LEXICAL ANALYSIS]")

    # Basic input checks
    if not isinstance(user_input, str):
        _err("input is not a string.")
        return []
    s = user_input.strip()
    if not s:
        _err("empty input.")
        return []

    # Full tokenization: ensure every character is consumed by known tokens
    tokens = []
    pos = 0
    n = len(s)

    while pos < n:
        m = _MASTER.match(s, pos)
        if not m:
            # Unknown/invalid character at pos
            snippet = s[pos:pos+10]
            _err(f"invalid token starting at position {pos}: {snippet!r}")
            return []
        kind = m.lastgroup
        lexeme = m.group()
        pos = m.end()

        # Safety: reject anything not in the allowed set (shouldn’t happen with the master regex)
        if kind not in _ALLOWED_KINDS:
            _err(f"disallowed token kind {kind} for lexeme {lexeme!r}")
            return []

        if kind == "WS":
            continue
        tokens.append((kind, lexeme))

    # Validate exact token sequence and count
    kinds_only = [k for k, _ in tokens]
    if kinds_only != _EXPECTED_SEQUENCE:
        _err(
            "invalid token sequence. Expected: "
            + " ".join(_EXPECTED_SEQUENCE)
            + f"  |  Found: {' '.join(kinds_only) if kinds_only else '<none>'}"
        )
        return []

    # Validate lexeme-level constraints
    type_lex = tokens[0][1]
    ident_lex = tokens[1][1]
    num1_lex  = tokens[3][1]
    op_lex    = tokens[4][1]
    num2_lex  = tokens[5][1]
    semi_lex  = tokens[6][1]

    # TYPE must be one of valid types (regex already enforces, but keep explicit)
    if type_lex not in _VALID_TYPES:
        _err(f"unknown type {type_lex!r}")
        return []

    # IDENT already alpha-only via regex; double-check for clarity
    if not re.fullmatch(r"[A-Za-z]+", ident_lex):
        _err("identifier must be alphabetic only")
        return []

    # OP must be in the allowed set
    if op_lex not in _VALID_OPS:
        _err(f"invalid operator {op_lex!r}")
        return []

    # NUMBERs: regex ensures format; we can sanity-cast to confirm validity
    try:
        float(num1_lex)
        float(num2_lex)
    except ValueError:
        _err("number literal not valid")
        return []

    # SEMICOLON lexeme must literally be ';' (it is by regex)
    if semi_lex != ";":
        _err("statement must end with ';'")
        return []

    # Success: print and return tokens
    for t in tokens:
        print(t)
    print()
    return tokens