import re

def lexical_analysis(filepath):
    # Define token categories
    keywords = {"if", "else", "while", "return", "int", "float", "char", "for", "break", "string", "continue"}
    operators = {"+", "-", "*", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||"}
    separators = {"(", ")", "{", "}", "[", "]", ";", ","}

    # Define the token pattern using regex
    token_pattern = r"""
        \d+(\.\d+)? |                      # Matches floating-point and integer numbers
        \"(?:\\.|[^"\\])*\" |               # Matches string literals with escape sequences
        [a-zA-Z_][a-zA-Z0-9_]* |            # Matches identifiers (variables, functions, etc.)
        (==|!=|<=|>=|\+=|-=|\*=|/=|&&|\|\|| # Matches multi-character operators
        [+\-*/=<>!&|;{}(),])                # Matches single-character operators and symbols
    """

    # Compile regex with VERBOSE mode for readability
    token_regex = re.compile(token_pattern, re.VERBOSE)

    try:
        # Read the file content
        with open(filepath, "r") as file:
            code = file.read()

        # Tokenize input code using `finditer` instead of `findall`
        tokens = [match.group(0) for match in token_regex.finditer(code)]

        # Categorize tokens
        categorized_tokens = []
        for token in tokens:
            if token in keywords:
                category = "KEYWORD"
            elif token in operators:
                category = "OPERATOR"
            elif token in separators:
                category = "SEPARATOR"
            elif re.fullmatch(r"\d+(\.\d+)?", token):
                category = "NUMBER"
            elif re.fullmatch(r"\"(?:\\.|[^\"\\])*\"", token):
                category = "STRING_LITERAL"
            else:
                category = "IDENTIFIER"
            
            categorized_tokens.append((token, category))

        # Display meaningful pieces (tokens)
        print("\n--- Lexical Analysis Output ---")
        for token, category in categorized_tokens:
            print(f"{token}: {category}")

    except FileNotFoundError:
        print("Error: File not found. Please provide a valid file path.")

# Example usage
file_path = input("Enter the file path: ")  # User provides file path
lexical_analysis(file_path)

