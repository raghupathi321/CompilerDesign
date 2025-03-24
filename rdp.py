class RecursiveDescentParser:
    def __init__(self, input_string):
        self.input = input_string.replace(" ", "")  # Remove spaces
        self.index = 0

    def error(self):
        raise SyntaxError(f"Syntax error at position {self.index}")

    def match(self, expected):
        if self.index < len(self.input) and self.input[self.index] == expected:
            self.index += 1
        else:
            self.error()

    def E(self):
        self.T()
        self.E_prime()

    def E_prime(self):
        if self.index < len(self.input) and self.input[self.index] == '+':
            self.match('+')
            self.T()
            self.E_prime()
        # epsilon (do nothing)

    def T(self):
        if self.index < len(self.input) and self.input[self.index].isdigit():
            self.match(self.input[self.index])  # Match a digit (number)
        else:
            self.error()

    def parse(self):
        self.E()
        if self.index == len(self.input):
            print("Parsing successful!")
        else:
            self.error()

if __name__ == "__main__":
    expression = input("Enter an arithmetic expression: ")
    parser = RecursiveDescentParser(expression)
    try:
        parser.parse()
    except SyntaxError as e:
        print(e)

