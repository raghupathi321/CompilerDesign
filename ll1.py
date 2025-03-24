from collections import defaultdict
import re

# Define the grammar
grammar = {
    'E': [['T', "E'"]],
    "E'": [['+', 'T', "E'"], ['ε']],
    'T': [['F', "T'"]],
    "T'": [['*', 'F', "T'"], ['ε']],
    'F': [['(', 'E', ')'], ['id']]
}

# Function to compute FIRST sets
def compute_first(grammar):
    first = defaultdict(set)

    def find_first(symbol):
        if symbol in first and first[symbol]:
            return first[symbol]
        if not symbol.isupper():  # Terminal
            first[symbol] = {symbol}
            return first[symbol]

        for production in grammar[symbol]:
            for token in production:
                token_first = find_first(token)
                first[symbol].update(token_first - {'ε'})
                if 'ε' not in token_first:
                    break
            else:
                first[symbol].add('ε')
        return first[symbol]

    for non_terminal in grammar:
        find_first(non_terminal)

    return first

# Function to compute FOLLOW sets
def compute_follow(grammar, first_sets):
    follow = defaultdict(set)
    start_symbol = next(iter(grammar))
    follow[start_symbol].add('$')  # Add end-of-input marker

    changed = True
    while changed:
        changed = False

        for non_terminal, productions in grammar.items():
            for production in productions:
                trailer = follow[non_terminal].copy()
                for i in range(len(production) - 1, -1, -1):
                    symbol = production[i]
                    if symbol.isupper():  # Non-terminal
                        if trailer - follow[symbol]:  # If new elements are added
                            follow[symbol].update(trailer)
                            changed = True
                        if 'ε' in first_sets[symbol]:
                            trailer.update(first_sets[symbol] - {'ε'})
                        else:
                            trailer = first_sets[symbol]
                    else:
                        trailer = {symbol}  # Reset for terminals

    return follow

# Function to build the LL(1) Parsing Table
def build_parsing_table(grammar, first_sets, follow_sets):
    table = {}

    for non_terminal, productions in grammar.items():
        for production in productions:
            first_of_production = set()
            for symbol in production:
                first_of_symbol = first_sets[symbol]
                first_of_production.update(first_of_symbol - {'ε'})
                if 'ε' not in first_of_symbol:
                    break
            else:
                first_of_production.update(follow_sets[non_terminal])  # If ε in all

            for terminal in first_of_production:
                table[(non_terminal, terminal)] = production

    return table

# Function to print Parsing Table
def print_parsing_table():
    print("\nParsing Table:")
    print("{:<8} {:<15} {:<20}".format("Non-Term", "Terminal", "Production"))
    print("-" * 50)
    for key, value in sorted(parsing_table.items()):
        print("{:<8} {:<15} -> {:<20}".format(key[0], key[1], " ".join(value)))
    print("-" * 50)

# Function to parse input using LL(1) Table
def parse(input_tokens):
    stack = ["$", "E"]
    pointer = 0
    print("\nParsing Steps:")
    print("{:<30} {:<30} {:<20}".format("Stack", "Input", "Action"))
    print("-" * 80)

    while stack:
        top = stack.pop()
        current_token = input_tokens[pointer]
        print("{:<30} {:<30}".format(" ".join(stack), " ".join(input_tokens[pointer:])), end=" ")

        if top == current_token:  # If matched, consume input
            print(f"Matched {current_token}")
            pointer += 1
            continue

        if top in grammar:  # If top of stack is a non-terminal
            production = parsing_table.get((top, current_token))

            if production is None:
                print("ERROR: Unexpected token")
                return False

            if production == ["ε"]:
                print(f"Expand {top} → ε")
                continue
            else:
                print(f"Expand {top} → {' '.join(production)}")
                stack.extend(reversed(production))
        else:
            print("ERROR: Unexpected token")
            return False

    print("-" * 80)
    return pointer == len(input_tokens)

# Function to tokenize input expression
def tokenize(expression):
    tokens = re.findall(r'\d+|id|[()+*]', expression)
    return tokens + ['$']  # Append end marker

# Main Execution
first_sets = compute_first(grammar)
follow_sets = compute_follow(grammar, first_sets)
parsing_table = build_parsing_table(grammar, first_sets, follow_sets)

# Display FIRST and FOLLOW sets
print("\nComputed First Sets:")
for non_terminal, first in first_sets.items():
    print(f"First({non_terminal}) = {first}")

print("\nComputed Follow Sets:")
for non_terminal, follow in follow_sets.items():
    print(f"Follow({non_terminal}) = {follow}")

print_parsing_table()

# Example Parsing
expression = "id+id*id"
input_tokens = tokenize(expression)
print("\nTokenized Input:", input_tokens)

if parse(input_tokens):
    print("\nParsing successful!")
else:
    print("\nParsing failed.")

