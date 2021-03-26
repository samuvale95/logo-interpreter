grammar logoGrammar;

prog: (line? EOL)* line?;

line:
	(graphic | controlStructure | arithmBoolOperations | procedureDeclaration | procedureInvocation | sys) +;

sys:
	pr     
	| make
	;

graphic:
	fd
	| bk
	| rt
	| lt
	| cs
	| pu
	| pd
	| ht
	| st
	| home
	| setxy
	| setpos
	| setx
	| sety
	| seth
	| arc
	| setpencolor
	| setpensize
	| clean
    ;

controlStructure:
	repeat		
	| if_	
	| ifelse	
	| while_	
	| stop	
	| output
	;

arithmBoolOperations:
	sum_
	| difference
	| product
	| quotient
	| remainder
	| modulo
	| int_
	| round_
	| sqrt_
	| power
	| exp
	| log10
	| ln
	| radsin
	| sin
	| cos
	| radcos
	| arctan
	| radarctan
	| lessp
	| graterp
	| lessequalp
	| graterequalp
	| random
	| rerandom
	| and_
	| or_
	| not_
	| minus
	;

/***************** OPERATORS *******************************/
addsuboperators: '+' | '-';

muldivoperators: '*' | '/';

comparisonOperator: '<' | '>' | '=' | '>=' | '<=';

/***************** NUMERIC EXPRESSION **********************/
expression:
	('+' | '-')* number
	| STRINGLITERAL
	| Boolean_
	|('+' | '-')* deref
	| rw
	| expression EOL* muldivoperators EOL* expression
	| expression EOL* addsuboperators EOL* expression
	| expression EOL* comparisonOperator EOL* expression
	| controlStructure
	| procedureInvocation
	| arithmBoolOperations
	| not_
	| and_
	| or_
	| ('+' | '-')* '(' expression ')'
	;
/***************** COMUNICATION ****************************/
pr:
	('PRINT' | 'print' | 'PR' | 'pr') EOL* (expression  | graphic)
	| '(' ('PRINT' | 'print' | 'PR' | 'pr') EOL* (expression  | graphic) EOL* ((expression  | graphic ) EOL*)+  EOL* ')';

rw: ('RW' | 'rw') | ('READWORD' | 'readword');

/***************** ARITHMETIC ******************************/
/* NUMERIC OPERATIONS */
sum_:
	('SUM' | 'sum') EOL* expression EOL* expression
	| '(' EOL* ('SUM' | 'sum') EOL* expression EOL* (expression EOL*)+ EOL*')';

difference: ('DIFFERENCE' | 'difference') EOL* expression EOL* expression;

minus: ('MINUS' | 'minus') EOL* expression;

quotient:
	('QUOTIENT' | 'quotient') EOL* expression EOL* expression
	| '(' EOL* ('QUOTIENT' | 'quotient') EOL* expression EOL* ')';

remainder: ('REMAINDER' | 'remainder') EOL* expression EOL* expression;

modulo: ('MODULO' | 'modulo') EOL* expression EOL* expression;

int_: ('INT' | 'int') EOL* expression;

round_: ('ROUND' | 'round') EOL* expression;

sqrt_: ('SQRT' | 'sqrt') EOL* expression;

power: ('POWER' | 'power') EOL* expression EOL* expression;

exp: ('EXP' | 'exp') EOL* expression;

log10: ('LOG10' | 'log10') EOL* expression;

ln: ('LN' | 'ln') EOL* expression;

sin: ('SIN' | 'sin') EOL* expression;

radsin: ('RADSIN' | 'radsin') EOL* expression;

cos: ('COS' | 'cos') EOL* expression;

radcos: ('RADCOS' | 'radcos') EOL* expression;

arctan:
	('ARCTAN' | 'arctan') EOL* expression
	| '(' EOL* ('ARCTAN' | 'arctan') EOL* expression EOL* expression EOL* ')';

radarctan:
	('RADARCTAN' | 'radarctan') EOL* expression
	| '(' EOL* ('RADARCTAN' | 'radarctan') EOL* expression EOL* expression EOL* ')';

product:
	('PRODUCT' | 'product') EOL* expression EOL* expression
	| '(' EOL* ('PRODUCT' | 'product') EOL* expression EOL* expression+ EOL* ')';

/* PREDICATES */
lessp: 
	('LESSP' | 'lessp') EOL* expression EOL* expression
	| ('LESS?' | 'less?') EOL* expression EOL* expression;

graterp: 
	('GREATERP' | 'graterp') EOL* expression EOL* expression
	| ('GREATER?' | 'grater?') EOL* expression EOL* expression;

lessequalp: 
	('LESSEQUALP' | 'lessequalp') EOL* expression EOL* expression
	| ('LESSEQUAL?' | 'lessequal?') EOL* expression EOL* expression;

graterequalp: 
	('GREATEREQUALP' | 'graterequalp') EOL* expression EOL* expression
	| ('GREATEREQUAL?' | 'graterequal?') EOL* expression EOL* expression;

/* RANDOM NUMBERS */
random:
	('RANDOM' | 'random') EOL* expression
	| '(' EOL* ('RANDOM' | 'random') EOL* expression EOL* expression EOL* ')';

rerandom: 
    ('RERANDOM' | 'rerandom')
	| '(' EOL* ('RERANDOM' | 'rerandom') EOL*  expression EOL* ')';

/****************** LOGICAL OPERATIONS *********************/
and_:
	('AND' | 'and') EOL* (expression | block) EOL* (expression | block)
	| '(' EOL* ('AND' | 'and') EOL* (expression | block) EOL* (expression | block )  EOL* ((expression |block) EOL* )+ EOL* ')';

or_:
	('OR' | 'or') EOL* (expression | block) EOL* (expression | block)
	| '(' EOL* ('OR' | 'or') (expression | block) EOL* (expression | block) EOL* ((expression | block) EOL*) + EOL* ')';

not_: ('NOT' | 'not') EOL* (expression | block);

/****************** GRAPHICS *******************************/
/* TURTLE MOTION */
fd: ('FD' | 'fd' | 'FORWARD' | 'forward') EOL* expression;

bk: ('BK' | 'bk' | 'BACK' | 'back') EOL* expression;

lt: ('LT' | 'lt' | 'LEFT' | 'left') EOL* expression;

rt: ('RT' | 'rt' | 'RIGHT' | 'right') EOL* expression;

setpos: ('SETPOS' | 'setpos') EOL* expression;

setxy: ('SETXY' | 'setxy') EOL* expression expression;

setx: ('SETX' | 'setx') EOL* expression;

sety: ('SETY' | 'sety') EOL* expression;

seth: ('SETH' | 'seth' | 'SETHEADING' | 'setheading') EOL* expression;

home: ('HOME' | 'home');

arc: ('ARC' | 'arc') EOL* expression EOL* expression;

/* TURTLE AND WINDOW CONTROL */
st: ('ST' | 'st' | 'SHOWTURTLE' | 'showturtle');

ht: ('HT' | 'ht' | 'HIDETURTLE' | 'hideturtle');

clean: ('CLEAN' | 'clean');

cs: ('CS' | 'cs' | 'CLEARSCREEN' | 'clearscreen');

/* PEN AND BACKGROUND CONTROL */
setpensize: ('SETPENSIZE' | 'setpensize') EOL* expression;

setpencolor: ('SETPENCOLOR' | 'setpencolor' | 'SETPC' | 'setpc') EOL* block;

pu: ('PU' | 'pu' | 'PENUP' | 'penup');

pd: ('PD' | 'pd' | 'PENDOWN' | 'pendown');

/****************** WORKSPACE MANAGEMENT *******************/
/* VARIABLE DEFINITION */
make: ('MAKE' | 'make') (STRINGLITERAL | deref) EOL* (expression  | graphic);

deref: ( ':' | 'THING' | 'thing' ) (deref | name | STRINGLITERAL);

/* PROCEDURE DEFINITION */
parameterDeclarations: ':' name EOL*;

procedureDeclaration:
	('TO' | 'to') EOL* name EOL* parameterDeclarations*  (line? EOL)+ ('END' | 'end');

/* PROCEDURE INVOCATION */
parameters:
	expression
	| '(' procedureInvocation ')'
	| procedureInvocation;

procedureInvocation:
	'(' name ')'
	| name EOL* parameters
	| '(' name EOL* parameters ')'
	| '(' name EOL* parameters EOL* parameters+ ')';

/****************** CONTROL STRUCTURES *********************/
if_: ('IF' | 'if') EOL* (expression | block) EOL* block;

ifelse: ('IFELSE' | 'ifelse') EOL* (expression | block) EOL* block block;

while_: ('WHILE' | 'while') EOL* (expression) EOL* block;

repeat: ('REPEAT' | 'repeat') EOL* expression EOL* block;

stop: ('STOP' | 'stop');

output: ('OUTPUT' | 'output' | 'OP' | 'op' ) EOL* (expression | graphic);

/****************** PRIMITIVE STRUCTURE ********************/
block:
	'[' EOL* (( graphic | expression | sys) EOL* )+ EOL* ']';

number: INT | FLOAT;

name: STRING ;

Boolean_: '"'?(T R U E | F A L S E);
fragment A:('a'|'A');
fragment E:('e'|'E');
fragment F:('f'|'F');
fragment L:('l'|'L');
fragment R:('r'|'R');
fragment S:('s'|'S');
fragment T:('t'|'T');
fragment U:('u'|'U');

STRINGLITERAL: '"' STRING;

STRING: [a-zA-Z] [a-zA-Z0-9_]*;

INT: [0-9]+;

FLOAT: [0-9]* '.'? [0-9]+;

EOL: '\r'? '\n';

WS: [ \t\r\n] -> skip;