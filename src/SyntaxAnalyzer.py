"""
 ===== SyntaxAnalyzer.py =====

The syntax analyzer is repsonsible for checking the grammatical
structure of a sentence or code, ensuring that it follows the rules of the language

Syntax Analyzer MUST receive the token list from the lexical analyzer
Syntax Output:
A abstract syntax tree captures the structure of the statement

The AST is then passed to the semantic and intermediate code generator for processing

Needs to return a dict in the format:
{
    "type": "int",
    "identifier": "y",
    "expression": {
        "op": "+",
        "left": 4,
        "right": 3
    }
}
"""
"""
def test_syntax(token_list):
    print("Testing Syntax Analyzer")
    
    return {}
"""

# The syntax analyzer checks the grammatical structure of a single statement of the form:
#   TYPE IDENT = NUMBER OP NUMBER ;
# and produces an AST dict:
# {
#     "type": "int" | "double",
#     "identifier": "<name>",
#     "expression": {"op": "+|-|*|/", "left": <num>, "right": <num>}
# }
#
# It assumes token_list comes from the lexical analyzer as a list of (KIND, LEXEME).
# KINDs expected: TYPE, IDENT, ASSIGN, NUMBER (or INT/FLOAT), OP, SEMICOLON
# On success: prints AST and returns it
# On failure: prints an error and returns {}

from typing import List, Tuple, Dict, Any
import re

_NUM_KINDS = {"NUMBER", "INT", "FLOAT"}   # support either style from the lexer
_EXPECTED_SEQUENCE = ["TYPE", "IDENT", "ASSIGN", "NUMBER", "OP", "NUMBER", "SEMICOLON"]
_EXPECTED_KINDS = ["TYPE", "IDENT", "ASSIGN", "NUM", "OP", "NUM", "SEMICOLON"]
_VALID_TYPES = {"int", "double"}
_VALID_OPS = {"+", "-", "*", "/"}

def _err(msg: str):
    print(f"Syntax error: {msg}")

def _to_number(lexeme: str):
    # Convert NUMBER lexeme to int or float
    try:
        if "." in lexeme:
            return float(lexeme)
        return int(lexeme)
    except ValueError:
        # Should not happen if lexer was correct, but guard anyway
        return None

# Validate exact token sequence and count
def validate_token_sequence(tokens):
      # Validate exact token sequence and count
    kinds_only = [k for k, _ in tokens]
    if kinds_only != _EXPECTED_SEQUENCE:
        _err(
            "invalid token sequence. Expected: "
            + " ".join(_EXPECTED_SEQUENCE)
            + f"  |  Found: {' '.join(kinds_only) if kinds_only else '<none>'}"
        )
        return [] 
    
def validate_types(tokens):
    # Make sure there are enough tokens before indexing
    if len(tokens) < 7:
        _err("too few tokens to validate types.")
        return False

    type_lex = tokens[0][1]
    ident_lex = tokens[1][1]
    num1_lex  = tokens[3][1]
    op_lex    = tokens[4][1]
    num2_lex  = tokens[5][1]
    semi_lex  = tokens[6][1]

    if type_lex not in _VALID_TYPES:
        _err(f"unknown type {type_lex!r}")
        return False
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", ident_lex):
        _err("identifier must be alphanumeric starting with alpha character only")
        return False
    if op_lex not in _VALID_OPS:
        _err(f"invalid operator {op_lex!r}")
        return False
    try:
        float(num1_lex)
        float(num2_lex)
    except ValueError:
        _err("number literal not valid")
        return False
    if semi_lex != ";":
        _err("statement must end with ';'")
        return False

    return True

def test_syntax(token_list: List[Tuple[str, str]]) -> Dict[str, Any]:
    print("[SYNTAX ANALYSIS]")

    if not token_list:
        _err("no tokens provided.")
        return {}
    
    # Validate token sequence
    validate_token_sequence(token_list)
    validate_types(token_list)
    
    if not validate_types:
        return {}

    # Must be exactly seven tokens: TYPE IDENT ASSIGN NUM OP NUM SEMICOLON
    if len(token_list) != 7:
        kinds = " ".join(k for k, _ in token_list)
        _err(f"expected 7 tokens (TYPE IDENT ASSIGN NUM OP NUM SEMICOLON); found {len(token_list)} -> {kinds}")
        return {}

    (k0, t_lex), (k1, id_lex), (k2, _eq), (k3, left_lex), (k4, op_lex), (k5, right_lex), (k6, semi_lex) = token_list

    # Kind checks in fixed positions
    if k0 != "TYPE":
        _err(f"expected TYPE at position 0; found {k0}")
        return {}
    if k1 != "IDENT":
        _err(f"expected IDENT at position 1; found {k1}")
        return {}
    if k2 != "ASSIGN":
        _err(f"expected ASSIGN '=' at position 2; found {k2}")
        return {}
    if k3 not in _NUM_KINDS:
        _err(f"expected NUMBER at position 3; found {k3}")
        return {}
    if k4 != "OP":
        _err(f"expected OP at position 4; found {k4}")
        return {}
    if k5 not in _NUM_KINDS:
        _err(f"expected NUMBER at position 5; found {k5}")
        return {}
    if k6 != "SEMICOLON" or semi_lex != ";":
        _err("statement must end with ';'")
        return {}

    # Operator validation
    if op_lex not in _VALID_OPS:
        _err(f"invalid operator '{op_lex}'")
        return {}

    # Convert numeric lexemes
    left_val = _to_number(left_lex)
    right_val = _to_number(right_lex)
    if left_val is None or right_val is None:
        _err("invalid numeric literal.")
        return {}

    # Build AST
    ast = {
        "type": t_lex,               # 'int' or 'double'
        "identifier": id_lex,        # variable name
        "expression": {
            "op": op_lex,
            "left": left_val,
            "right": right_val
        }
    }

    # Print AST and return
    print("Syntax valid. AST:")
    print(ast)
    print()
    return ast

# ----------------------------------------------------------------------
# Test Suite for Syntax Analyzer
# ----------------------------------------------------------------------

def test_syntax_suite():
    print("\n===== Running Syntax Analyzer Test Suite =====\n")

    tests = [
        # Valid cases
        {
            "name": "Basic int addition",
            "input": [
                ("TYPE", "int"),
                ("IDENT", "y"),
                ("ASSIGN", "="),
                ("NUMBER", "4"),
                ("OP", "+"),
                ("NUMBER", "3"),
                ("SEMICOLON", ";")
            ],
            "expected": {
                "type": "int",
                "identifier": "y",
                "expression": {"op": "+", "left": 4, "right": 3}
            }
        },
        {
            "name": "Valid double multiplication",
            "input": [
                ("TYPE", "double"),
                ("IDENT", "area"),
                ("ASSIGN", "="),
                ("NUMBER", "3.5"),
                ("OP", "*"),
                ("NUMBER", "2"),
                ("SEMICOLON", ";")
            ],
            "expected": {
                "type": "double",
                "identifier": "area",
                "expression": {"op": "*", "left": 3.5, "right": 2}
            }
        },

        # Invalid cases
        {
            "name": "Missing semicolon",
            "input": [
                ("TYPE", "int"),
                ("IDENT", "x"),
                ("ASSIGN", "="),
                ("NUMBER", "5"),
                ("OP", "+"),
                ("NUMBER", "2"),
            ],
            "expected": {}  # should fail
        },
        {
            "name": "Invalid operator",
            "input": [
                ("TYPE", "int"),
                ("IDENT", "z"),
                ("ASSIGN", "="),
                ("NUMBER", "10"),
                ("OP", "%"),  # not allowed
                ("NUMBER", "3"),
                ("SEMICOLON", ";")
            ],
            "expected": {}  # should fail
        },
        {
            "name": "Unknown type",
            "input": [
                ("TYPE", "float"),  # invalid type for this grammar
                ("IDENT", "w"),
                ("ASSIGN", "="),
                ("NUMBER", "9"),
                ("OP", "-"),
                ("NUMBER", "2"),
                ("SEMICOLON", ";")
            ],
            "expected": {}  # should fail
        },
    ]

    passed = 0
    for case in tests:
        print(f"--- {case['name']} ---")
        result = test_syntax(case["input"])
        expected = case["expected"]
        if result == expected:
            print("PASS\n")
            passed += 1
        else:
            print("FAIL")
            print("Expected:", expected)
            print("Got:", result, "\n")

    print(f"Summary: {passed}/{len(tests)} tests passed.\n")


# ----------------------------------------------------------------------
# Run the suite if executed directly
# ----------------------------------------------------------------------
if __name__ == "__main__":
    test_syntax_suite()
