""" ==== math_solver.py ==== 
This project implements a one-way compiler that solves simple C++-style arithmetic expressions. 
The program accepts a single math expression containing exactly two operands and one operator. 
Supported operations include addition, subtraction, multiplication, and division. 
The operand types must match the declared variable type (e.g., int or double), and the compiler 
verifies type correctness before evaluating the expression.

The compiler contains for the following
[1] Lexical Analysis
[2] Syntax Analysis
[3] Semantic Analysis
[4] Intermediate code generation
[5] Assembler 

The input from the user must be in a C++ style format
int y = 4 + 3;   →   y = 7
int z = 3 * 4;   →   z = 12
double t = 4.0 * 3.1;   →   t = 12.1
double u = 9.2 / 2;     →   u = 4.6

REQUIREMENTS
[1] The type must be defined
[2] Expressions must end with a semicolon
[3] Defined type must match the variables passed
[4] Allow for parsing with or without spaces
[5] Variable must be alpha and operands must be a valid number
"""

from LexicalAnalyzer import test_lexical
from SyntaxAnalyzer import test_syntax
from SemanticAnalyzer import test_semantic
from IntermediateCodeGenerator import test_intermediate
from Assembler import test_assembler

def main():
    print("\nWelcome to Math Solver where we will solve your simple math.")
    print("Wrtie your math problem in the following format.")
    print("(type)(identifier)=(int/double)(operation +,-,*,/)(int/double);")
    print("Example 1: int x=1+1;")
    print("Example 2: double y=2.0+2.0;")
    print("The answer will be printed as x=2; y=4.0;")

    while True:
        user_input = input(
            "Enter a simple math expression (or type 'q' to quit): "
        ).strip()

        if user_input.lower() == 'q':
            print("Exiting program...")
            break

        if not user_input:
            print("Invalid input. Try again.\n")
            continue

        print("\n=== Starting Compilation Steps ===")

        # 1. LEXICAL ANALYSIS
        token_list = test_lexical(user_input)
        if not token_list:
            print("Lexical analysis failed.\n")
            print("=== Compilation Failed ===")
            continue

        # 2. SYNTAX ANALYSIS
        ast = test_syntax(token_list)
        if not ast:
            print("Syntax analysis failed.\n")
            print("=== Compilation Failed ===")
            continue

        # 3. SEMANTIC ANALYSIS
        if not test_semantic(ast):
            print("Semantic analysis failed.\n")
            print("=== Compilation Failed ===")
            continue

        # 4. INTERMEDIATE CODE GENERATION
        if not test_intermediate(ast):
            print("Intermediate code generation failed.\n")
            print("=== Compilation Failed ===")
            continue

        # 5. ASSEMBLER
        if not test_assembler(ast):
            print("Assembly generation failed.\n")
            print("=== Compilation Failed ===")
            continue

        print("=== Compilation Successfully Completed ===\n")

if __name__ == "__main__":
    main()
