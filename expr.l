%{
    #include "y.tab.h"
    #include <string.h>
%}
%%
[ \t]+                  { /* Ignore whitespace */ }
[a-zA-Z_][a-zA-Z_0-9]*  { strcpy(yylval.id_name, yytext); return ID; }
[0-9]+(\.[0-9]*)?       { yylval.num_val = atof(yytext); return NUM; }
[+\-*/()]               { return yytext[0]; }
"="                     { return '='; }
";"                     { return ';'; }
\n                      { return 0; }
.                       { return yytext[0]; }
%%
int yywrap() {
    return 1;
}

