"""
===== Assembler.py =====

The Assembler is responsible for converting the intermediate code
into low-level assembly instructions.

For integer operations → LD, ADD, ST
For double (float) operations → LDF, ADDF, STF

Print answer after calculation as example below
Answer: y=1;
"""

from typing import Dict, Any, List

# ----------------------------------------------------------------------
# Register Management
# ----------------------------------------------------------------------
_register_counter = 1

def _new_reg() -> str:
    """Generate a new register name."""
    global _register_counter
    reg = f"R{_register_counter}"
    _register_counter += 1
    return reg

# ----------------------------------------------------------------------
# Operation mapping by type
# ----------------------------------------------------------------------
_OP_MAP = {
   "int": {
       "load": "LD",
       "store": "ST",
       "add": "ADD",
       "sub": "SUB",
       "mul": "MUL",
       "div": "DIV"
   },
   "double": {
       "load": "LDF",
       "store": "STF",
       "add": "ADDF",
       "sub": "SUBF",
       "mul": "MULF",
       "div": "DIVF"
   }
}
# ----------------------------------------------------------------------
# Operation symbol -> mnemonic key
# ----------------------------------------------------------------------
def op_to_mnemonic(op: str) -> str:
   """Map arithmetic symbol to mnemonic keyword used in _OP_MAP."""
   return {
       "+": "add",
       "-": "sub",
       "*": "mul",
       "/": "div"
   }[op]


# ----------------------------------------------------------------------
# Compute the numeric result
# ----------------------------------------------------------------------
def _compute(var_type: str, op: str, left, right):
   """
   Perform the actual arithmetic based on the AST and return:
   (numeric_value, rendered_string)
   """
   # Work in Python numeric space
   a = left
   b = right


   if op == "+":
       res = a + b
   elif op == "-":
       res = a - b
   elif op == "*":
       res = a * b
   elif op == "/":
       res = a / b
   else:
       raise ValueError(f"Unknown operator {op!r}")


   # Render according to variable type
   if var_type == "int":
       # mimic C-like truncation for int
       res_int = int(res)
       return res_int, str(res_int)
   else:  # "double"
       res_float = float(res)
       # Format nicely (avoid too many trailing zeros)
       return res_float, f"{res_float:.12g}"


# ----------------------------------------------------------------------
# Assembly code generation
# ----------------------------------------------------------------------
def test_assembler(ast: Dict[str, Any]) -> List[str]:
   """
   Generate assembly code from AST and print the final result as: identifier=answer;
   AST format:
   {
       "type": "int" or "double",
       "identifier": "y",
       "expression": {
           "op": "+",
           "left": 4,
           "right": 3
       }
   }
   """
   print("[ASSEMBLER]")


   if not ast or "expression" not in ast:
       print("Assembly error: invalid AST.")
       return []


   var_type = ast.get("type", "int")
   expr = ast["expression"]
   op = expr["op"]
   left = expr["left"]
   right = expr["right"]
   identifier = ast["identifier"]


   if var_type not in _OP_MAP:
       print(f"Assembly error: unsupported type '{var_type}'.")
       return []


   ops = _OP_MAP[var_type]
   reg = _new_reg()


   # Generate pseudo-assembly
   code = [
       f"{ops['load']} {reg}, {left}",
       f"{ops[op_to_mnemonic(op)]} {reg}, {right}",
       f"{ops['store']} {identifier}, {reg}"
   ]


   # Print assembly
   for line in code:
       print(line)


   # Compute and print final result using the *user's* identifier
   _, rendered = _compute(var_type, op, left, right)
   print(f"\nAnswer: {identifier}={rendered};\n")


   return code


# ----------------------------------------------------------------------
# Test Suite
# ----------------------------------------------------------------------
def test_assembler_suite():
   print("===== Running Assembler Test Suite =====\n")


   # Reset register counter for predictable tests
   global _register_counter
   _register_counter = 1


   tests = [
       {
           "name": "Integer addition",
           "input": {
               "type": "int",
               "identifier": "y",
               "expression": {"op": "+", "left": 4, "right": 3}
           },
           "expected": ["LD R1, 4", "ADD R1, 3", "ST y, R1"]
       },
       {
           "name": "Double multiplication",
           "input": {
               "type": "double",
               "identifier": "area",
               "expression": {"op": "*", "left": 2.5, "right": 5.0}
           },
           "expected": ["LDF R2, 2.5", "MULF R2, 5.0", "STF area, R2"]
       }
   ]


   passed = 0
   for case in tests:
       print(f"--- {case['name']} ---")
       result = test_assembler(case["input"])
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
   test_assembler_suite()
