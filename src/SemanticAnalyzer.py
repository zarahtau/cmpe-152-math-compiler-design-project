"""
 ===== SemanticAnalyzer.py =====

SemanticAnalyzer is used to check the validity of the user input. After parsing/lexical
analysis, this code will be used for type check and making sure a variable
is declared before use. 

This is different from the Syntax analyzer in that we are checking the meaning of the structure for logical correctness.
A syntax analyzer is responsible for checking the grammatical structure of a sentence.

The requirements for this section are
[1] Type checking 
[2] Scope Resolution
[3] Symbol Table {created only if the first 2 pass}

The SemanticAnalyzer should flag if a user ensters int t = 4.0/2.0
"""

def test_semantic(user_input):
    print("Testing Semantic Analyzer")
    return True