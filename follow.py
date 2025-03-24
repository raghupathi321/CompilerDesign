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


def compute_follow(grammar, first_sets):
    follow = defaultdict(set)
    
    # Start symbol gets '$' in FOLLOW
    start_symbol = next(iter(grammar))
    follow[start_symbol].add('$')

    # Iteratively compute FOLLOW sets
    changed = True
    while changed:
        changed = False

        for non_terminal, productions in grammar.items():
            for production in productions:
                trailer = follow[non_terminal].copy()  # Start with FOLLOW(A)

                # Traverse the production from right to left
                for i in range(len(production) - 1, -1, -1):
                    symbol = production[i]

                    if symbol.isupper():  # Only compute FOLLOW for non-terminals
                        if trailer - follow[symbol]:  # Check if new elements are added
                            follow[symbol].update(trailer)
                            changed = True

                        if 'ε' in first_sets[symbol]:  
                            trailer.update(first_sets[symbol] - {'ε'})  # FIRST without ε
                        else:
                            trailer = first_sets[symbol]  # Update trailer with FIRST(symbol)
                    else:
                        trailer = {symbol}  # Reset trailer for terminals

    return follow


# Example Grammar Input
grammar = {
    'E': [['T', 'E\'']],
    'E\'': [['+', 'T', 'E\''], ['ε']],
    'T': [['F', 'T\'']],
    'T\'': [['*', 'F', 'T\''], ['ε']],
    'F': [['(', 'E', ')'], ['id']]
}

# Compute FIRST and FOLLOW sets
first_sets = compute_first(grammar)
follow_sets = compute_follow(grammar, first_sets)

# Print FIRST sets
print("\nFIRST Sets:")
for symbol, first_set in first_sets.items():
    print(f"FIRST({symbol}) = {{ {', '.join(first_set)} }}")

# Print FOLLOW sets
print("\nFOLLOW Sets:")
for symbol, follow_set in follow_sets.items():
    print(f"FOLLOW({symbol}) = {{ {', '.join(follow_set)} }}")

