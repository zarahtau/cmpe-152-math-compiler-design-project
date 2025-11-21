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

def test_semantic(user_input):
    print("Testing Semantic Analyzer")
    return True