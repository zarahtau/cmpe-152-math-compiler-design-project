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

If the LexicalAnalyzer is successful, the function will return true
"""


def test_lexical():
    print("testing lexical")
    
    # Return true if successful if not successful
