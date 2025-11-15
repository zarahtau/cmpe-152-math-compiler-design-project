#Main 

from LexicalAnalyzer import test_lexical
#Prompt for user inputs
while True:
    user_input = input("Enter a simple math problem. Example: y(variable)=4(number)+(type 'q' to exit): ").strip()

    # Exit condition
    if user_input.lower() == 'q':
        print("Exiting program...")
        break

# Defining main function
def main():
    print("hey there")
    
    test_lexical()


# Using the special variable 
# __name__
if __name__=="__main__":
    main()
    # Check for valid input
    if not user_input:
        print("Invalid input. Please try again following the valid input prompt.")
    else:
        print(f"Valid input: {user_input}")
