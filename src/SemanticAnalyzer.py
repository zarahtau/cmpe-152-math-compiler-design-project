"""
 ===== SemanticAnalyzer.py =====

SemanticAnalyzer is used to check the validity of the user input. After parsing/lexical
analysis, this code will be used for type check and making sure a variable
is declared before use. 

This is different from the Syntax analyzer in that we are checking the meaning of the structure for logical correctness.
A syntax analyzer is responsible for checking the grammatical structure of a sentence.

The semantic analyzer MUST receive Input from the Syntax Analyzer

Semantic Checks Include:
[1] Variable type matches expression type
[2] Numbers are allowed for the operation
[3] Operator is valid for the type (+, -, *, /)
[4] Dividing doubles and ints is allowed based on your rules

Semantic Output:
[1] True if valid
[2] False (or an error) if invalid
"""

"""def test_semantic(user_input):
    print("Testing Semantic Analyzer")
    return True
"""
# ===== SemanticAnalyzer.py =====
"""
SemanticAnalyzer is used to check the validity of the user input. After
syntax/lexical analysis, this code is used for type checking and making sure
the expression is logically correct.

Input AST format (from SyntaxAnalyzer):

{
    "type": "int" or "double",
    "identifier": "y",
    "expression": {
        "op": "+",       # one of +, -, *, /
        "left": 4,       # Python int or float literal
        "right": 3       # Python int or float literal
    }
}

Semantic checks:
[1] Variable type matches expression type (NO implicit promotion)
[2] Numbers are allowed for the operation
[3] Operator is valid (+, -, *, /)
[4] No mixed-type expressions: int op int OR double op double only
[5] Division by zero is forbidden

Output:
- True if valid
- False if invalid
"""

from typing import Dict, Any

_SYMBOL_TABLE: Dict[str, Dict[str, str]] = {}

VALID_TYPES = {"int", "double"}
VALID_OPS = {"+", "-", "*", "/"}


def _err(msg: str) -> None:
    print(f"Semantic error: {msg}")


def _infer_literal_type(value) -> str:
    """Infer 'int' or 'double' from a Python literal."""
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "double"
    return "unknown"


def test_semantic(ast: Dict[str, Any]) -> bool:
    print("[SEMANTIC ANALYSIS]")

    # Basic AST sanity
    if not isinstance(ast, dict):
        _err("AST is not a dictionary.")
        return False

    if "type" not in ast or "identifier" not in ast or "expression" not in ast:
        _err("AST missing required fields (type / identifier / expression).")
        return False

    declared_type = ast["type"]          # 'int' or 'double'
    var_name = ast["identifier"]
    expr = ast["expression"]

    if declared_type not in VALID_TYPES:
        _err(f"unknown declared type '{declared_type}'.")
        return False

    if not isinstance(var_name, str) or not var_name:
        _err("invalid identifier name.")
        return False

    # Expression structure
    if not isinstance(expr, dict) or not {"op", "left", "right"} <= expr.keys():
        _err("invalid expression node in AST.")
        return False

    op = expr["op"]
    left_val = expr["left"]
    right_val = expr["right"]

    # [3] Operator validity
    if op not in VALID_OPS:
        _err(f"operator '{op}' is not supported.")
        return False

    # [2] Numbers must be allowed (only numeric literals for now)
    if not isinstance(left_val, (int, float)):
        _err("left operand must be a numeric literal.")
        return False

    if not isinstance(right_val, (int, float)):
        _err("right operand must be a numeric literal.")
        return False

    # [5] Division by zero
    if op == "/" and float(right_val) == 0.0:
        _err("division by zero.")
        return False

    # Infer operand types
    left_type = _infer_literal_type(left_val)
    right_type = _infer_literal_type(right_val)

    if left_type == "unknown" or right_type == "unknown":
        _err("unable to infer operand types.")
        return False

    # [4] No mixed-type expressions
    if left_type != right_type:
        _err(
            f"mixed-type expression is not allowed: left is '{left_type}' "
            f"but right is '{right_type}'. Must use all int or all double expressions."
        )
        return False

    # Expression type is the common operand type
    expr_type = left_type

    # [1] Variable type must match expression type exactly
    if declared_type != expr_type:
        _err(
            f"mixed-type expression is not allowed: variable is '{declared_type}' but expression is '{expr_type}'. "
            "Only int→int and double→double assignments are allowed."
        )
        return False

    # If we reach here, semantics are valid; record variable type
    _SYMBOL_TABLE[var_name] = {"type": declared_type}

    print("Semantics valid.")
    print()
    return True
