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

_NUM_KINDS = {"NUMBER", "INT", "FLOAT"}   # support either style from your lexer
_EXPECTED_KINDS = ["TYPE", "IDENT", "ASSIGN", "NUM", "OP", "NUM", "SEMICOLON"]
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

def test_syntax(token_list: List[Tuple[str, str]]) -> Dict[str, Any]:
    print("[SYNTAX ANALYSIS]")

    if not token_list:
        _err("no tokens provided.")
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