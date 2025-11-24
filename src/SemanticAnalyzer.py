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

# SemanticAnalyzer checks meaning-level correctness:
# [1] Variable type matches expression type
# [2] Operands are numbers (for now, per your AST)
# [3] Operator is valid (+, -, *, /)
# [4] Division rules, including divide-by-zero
#
# Input: AST dict from SyntaxAnalyzer:
# {
#   "type": "int"|"double",
#   "identifier": "y",
#   "expression": {"op": "+|-|*|/", "left": <num>, "right": <num>}
# }
#
# Output: True (valid) or False (invalid)
#
# Notes:
# - Maintains a simple symbol table to support "declared before use" as you expand.
# - Current grammar uses numeric literals only; identifiers in expressions can be added later.

from typing import Dict, Any

# Global symbol table: var_name -> {"type": "int"|"double"}
_SYMTAB: Dict[str, Dict[str, str]] = {}

_VALID_TYPES = {"int", "double"}
_VALID_OPS = {"+", "-", "*", "/"}

def _err(msg: str) -> None:
    print(f"Semantic error: {msg}")

def _infer_number_type(n) -> str:
    """
    Infer 'int' or 'double' from a Python numeric literal in the AST.
    """
    if isinstance(n, int):
        return "int"
    if isinstance(n, float):
        return "double"
    # If you later allow identifiers, handle them here.
    return "unknown"

def _result_type(lhs_type: str, rhs_type: str, op: str) -> str:
    """
    Simple arithmetic promotion rules:
    - If either operand is double -> result is double
    - Else result is int
    - Division with two ints stays int (C-style integer division) for this project
      to match examples like: int z = 3 * 4; and allow int y = 4 / 2;
    """
    if lhs_type == "double" or rhs_type == "double":
        return "double"
    # both int
    return "int"

def test_semantic(ast: Dict[str, Any], symtab: Dict[str, Dict[str, str]] = None) -> bool:
    print("[SEMANTIC ANALYSIS]")

    # Use provided symtab or module-global one
    table = symtab if symtab is not None else _SYMTAB

    # Basic AST shape checks
    if not isinstance(ast, dict) or "type" not in ast or "identifier" not in ast or "expression" not in ast:
        _err("invalid AST shape.")
        return False

    declared_type = ast["type"]
    var_name = ast["identifier"]
    expr = ast["expression"]

    if declared_type not in _VALID_TYPES:
        _err(f"unknown type '{declared_type}'.")
        return False
    if not isinstance(var_name, str) or not var_name:
        _err("invalid identifier.")
        return False
    if not isinstance(expr, dict) or not {"op", "left", "right"} <= set(expr.keys()):
        _err("invalid expression node.")
        return False

    op = expr["op"]
    left = expr["left"]
    right = expr["right"]

    # [3] Operator validity
    if op not in _VALID_OPS:
        _err(f"operator '{op}' is not supported.")
        return False

    # [2] Numbers are allowed for the operation (current grammar uses numeric literals)
    if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
        _err("operands must be numeric literals for this grammar.")
        return False

    # Division by zero check (for both int and double)
    if op == "/" and float(right) == 0.0:
        _err("division by zero.")
        return False

    # Infer operand types
    lt = _infer_number_type(left)
    rt = _infer_number_type(right)
    if lt == "unknown" or rt == "unknown":
        _err("unable to infer operand type.")
        return False

    # Compute expression type
    expr_type = _result_type(lt, rt, op)

    # [4] Division rules:
    # - int / int is allowed; result considered 'int' in this project
    # - mixing int and double promotes to 'double' (already handled above)
    # (Already enforced via _result_type and checks below.)

    # [1] Variable type must match expression type
    if declared_type == "int" and expr_type == "double":
        _err("cannot assign a double expression to an int variable.")
        return False

    # If we reach here, semantics are valid. "Declare" the variable.
    table[var_name] = {"type": declared_type}

    print("Types valid and semantics OK.")
    print()
    return True