"""
 ===== Assembler.py =====

The assembler is used to map the user input and map data to the equivalent assembly

This is different from the Syntax analyzer in that we are checking the meaning of the structure for logical correctness.
A syntax analyzer is responsible for checking the grammatical structure of a sentence.

The requirements for this section are
[1] Type checking 
[2] Scope Resolution
[3] Symbol Table {created only if the first 2 pass}

The SemanticAnalyzer should flag if a user ensters int t = 4.0/2.0
"""

def test_assembler(user_input):
    print("Testing Assembler")
    
    # Return true if successful if not successful
    return True