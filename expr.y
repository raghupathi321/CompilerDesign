%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    int yylex();
    void yyerror(const char *msg);

    // Define a simple symbol table
    struct SymbolTable {
        char name[50];
        double value;
    } symbols[100];

    int symbolCount = 0;

    // Function to store a variable's value
    void storeVariable(char* name, double value) {
        for (int i = 0; i < symbolCount; i++) {
            if (strcmp(symbols[i].name, name) == 0) {
                symbols[i].value = value;
                return;
            }
        }
        strcpy(symbols[symbolCount].name, name);
        symbols[symbolCount].value = value;
        symbolCount++;
    }

    // Function to retrieve a variable's value
    double getVariable(char* name) {
        for (int i = 0; i < symbolCount; i++) {
            if (strcmp(symbols[i].name, name) == 0) {
                return symbols[i].value;
            }
        }
        yyerror("Undefined variable!");
        return 0;
    }
%}

%union {
    double num_val;
    char id_name[50];
}

%token <num_val> NUM
%token <id_name> ID
%type <num_val> expr term factor

%%

statement : ID '=' expr ';' { 
                storeVariable($1, $3);
                printf("\nValid expression! Result = %.2f\n", $3);
            }
          ;

expr  : term                 { $$ = $1; }
      | expr '+' term        { $$ = $1 + $3; }
      | expr '-' term        { $$ = $1 - $3; }
      ;

term  : factor               { $$ = $1; }
      | term '*' factor      { $$ = $1 * $3; }
      | term '/' factor      { 
            if ($3 == 0) {
                yyerror("Division by zero!");
                $$ = 0;
            } else {
                $$ = $1 / $3;
            }
        }
      ;

factor: NUM                  { $$ = $1; }
      | ID                   { $$ = getVariable($1); }
      | '(' expr ')'         { $$ = $2; }
      | '-' factor           { $$ = -$2; }
      ;

%%

void yyerror(const char *msg) {
    printf("\nError: %s\n", msg);
}

int main() {
    printf("\nEnter the expression:\n");
    yyparse();
    return 0;
}

