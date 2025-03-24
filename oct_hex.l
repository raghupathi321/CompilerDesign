%{
#include <stdio.h>
int is_octal = 0;
int is_hex = 0;
%}

DIGIT       [0-7]
HEX_DIGIT   [0-9a-fA-F]

%%

0{DIGIT}+           { is_octal = 1; printf("'%s' is an Octal number\n", yytext); }
0[xX]{HEX_DIGIT}+   { is_hex = 1; printf("'%s' is a Hexadecimal number\n", yytext); }
[0-9]+              { printf("'%s' is neither a valid Octal nor Hexadecimal number\n", yytext); }
.|\n                { /* ignore other characters */ }

%%

int main() {
    printf("Enter a number (octal starts with 0, hex starts with 0x or 0X): ");
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}
