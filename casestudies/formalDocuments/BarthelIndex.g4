grammar BarthelIndex;

startRule 
   : biTable EOF
   ;

biTable
   : biItem+
   ;

biItem
   : integerLiteral '.' text (integerLiteral | integerRange) integerLiteral
   ;

integerLiteral
   : INTEGERLITERAL 
   ;

integerRange
   : INTEGERLITERAL '-' INTEGERLITERAL
   ;

text
   : NONNUMERICCHARACTERS
   ; 

fragment STRINGLITERAL :
	'"' (~["\n\r] | '""' | '\'')* '"'
	| '\'' (~['\n\r] | '\'\'' | '"')* '\''
;


INTEGERLITERAL : [0-9]+;

NONNUMERICCHARACTERS : [a-zA-Z][a-zA-Z= (),;_]+;

// whitespace, line breaks, comments, ...
NEWLINE : '\r'? '\n' -> channel(HIDDEN);
WS : [ \t\f;]+ -> channel(HIDDEN);
SEPARATOR : ', ' -> channel(HIDDEN);

