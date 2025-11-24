"""
===== IntermediateCodeGenerator.py =====

After the lexical, semantic, and syntax analyzers have passed,
the intermediate code generator is responsible for translating the source code
into an intermediate representation (IR).

This intermediate code is a lower-level, platform-independent
representation that will be passed to the assembler or optimizer
for translation to machine code.

Expected Input (AST from Syntax Analyzer):
{
    "type": "int",
    "identifier": "y",
    "expression": {
        "op": "+",
        "left": 4,
        "right": 3
    }
}

Expected Output (Three Address Code):
t1 = 4 + 3
y = t1
"""

from typing import Dict, Any, List

# ----------------------------------------------------------------------
# Temporary variable generator
# ----------------------------------------------------------------------
_temp_counter = 1

def _new_temp() -> str:
    """Generate a new temporary variable name."""
    global _temp_counter
    name = f"t{_temp_counter}"
    _temp_counter += 1
    return name

# ----------------------------------------------------------------------
# Expression code generation
# ----------------------------------------------------------------------
def _generate_expression(expr: Any, code: List[str]) -> str:
    """
    Recursively generate code for an expression node.
    Returns the temporary variable name (or value) holding the result.
    """
    # Base case: direct number (int/float)
    if isinstance(expr, (int, float)):
        return str(expr)

    # Recursive case: expression node
    op = expr.get("op")
    left = expr.get("left")
    right = expr.get("right")

    left_var = _generate_expression(left, code) if isinstance(left, dict) else str(left)
    right_var = _generate_expression(right, code) if isinstance(right, dict) else str(right)

    temp = _new_temp()
    code.append(f"{temp} = {left_var} {op} {right_var}")
    return temp

# ----------------------------------------------------------------------
# Main Intermediate Code Generator
# ----------------------------------------------------------------------
def test_intermediate(ast: Dict[str, Any]) -> List[str]:
    """
    Generate intermediate (three-address) code from the AST.
    Returns a list of code lines.
    """
    print("[INTERMEDIATE CODE GENERATION]")

    if not ast or "expression" not in ast or "identifier" not in ast:
        print("Intermediate code error: invalid AST.")
        return []

    code: List[str] = []
    temp_result = _generate_expression(ast["expression"], code)
    code.append(f"{ast['identifier']} = {temp_result}")

    for line in code:
        print(line)
    print()

    return code

# ----------------------------------------------------------------------
# Test Suite for Intermediate Code Generator
# ----------------------------------------------------------------------
def test_intermediate_suite():
    print("===== Running Intermediate Code Generator Test Suite =====\n")

    tests = [
        {
            "name": "Simple addition",
            "input": {
                "type": "int",
                "identifier": "y",
                "expression": {"op": "+", "left": 4, "right": 3}
            },
            "expected": ["t1 = 4 + 3", "y = t1"]
        },
        {
            "name": "Nested expression",
            "input": {
                "type": "int",
                "identifier": "z",
                "expression": {
                    "op": "*",
                    "left": {"op": "+", "left": 2, "right": 3},
                    "right": 5
                }
            },
            "expected": ["t1 = 2 + 3", "t2 = t1 * 5", "z = t2"]
        },
        {
            "name": "Invalid AST",
            "input": {},
            "expected": []
        }
    ]

    passed = 0
    for case in tests:
        print(f"--- {case['name']} ---")
        result = test_intermediate(case["input"])
        if result == case["expected"]:
            print("PASS\n")
            passed += 1
        else:
            print("FAIL")
            print("Expected:", case["expected"])
            print("Got:", result, "\n")

    print(f"Summary: {passed}/{len(tests)} tests passed.\n")


# ----------------------------------------------------------------------
# Run suite if executed directly
# ----------------------------------------------------------------------
if __name__ == "__main__":
    test_intermediate_suite()
