from collections import defaultdict

def compute_first(grammar):
    first = defaultdict(set)

    def find_first(symbol):
        # If already computed, return it
        if symbol in first and first[symbol]:
            return first[symbol]

        # If terminal, FIRST(symbol) is itself
        if not symbol.isupper():
            first[symbol] = {symbol}
            return first[symbol]

        # Compute FIRST for non-terminal symbol
        for production in grammar[symbol]:
            for token in production:
                token_first = find_first(token)
                first[symbol].update(token_first - {'ε'})  # Add everything except ε
                
                if 'ε' not in token_first:
                    break  # Stop if ε is not found in token
            else:
                first[symbol].add('ε')  # Add ε if all symbols in production can be ε
        
        return first[symbol]

    # Compute FIRST for each non-terminal
    for non_terminal in grammar:
        find_first(non_terminal)

    return first

# Example Grammar Input
grammar = {
    'E': [['T', 'E\'']],
    'E\'': [['+', 'T', 'E\''], ['ε']],
    'T': [['F', 'T\'']],
    'T\'': [['*', 'F', 'T\''], ['ε']],
    'F': [['(', 'E', ')'], ['id']]
}

# Compute FIRST sets
first_sets = compute_first(grammar)

# Print FIRST sets
for symbol, first_set in first_sets.items():
    print(f"FIRST({symbol}) = {{ {', '.join(first_set)} }}")

