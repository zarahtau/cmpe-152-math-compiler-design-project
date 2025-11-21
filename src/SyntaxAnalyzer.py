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

def test_syntax(token_list):
    print("Testing Syntax Analyzer")
    
    return {}