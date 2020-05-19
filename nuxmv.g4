grammar nuxmv;

nuxmv : module*;
/*
 * Lexer Rules
 fragments: they are reusable building blocks for lexer rules
 */
// fragment M : ('M'|'m'); //MODULE
// fragment O : ('O'|'o');
// fragment D : ('D'|'d');
// fragment U : ('U'|'u');
// fragment L : ('L'|'l');
// fragment E : ('E'|'e');
// fragment V : ('V'|'v'); //VAR
// fragment A : ('A'|'a');
// fragment R : ('R'|'r');
// fragment S : ('S'|'s'); //ASSIGN
// fragment I : ('I'|'i');
// fragment G : ('G'|'g');
// fragment N : ('N'|'n');

 fragment LOWERCASE  : [a-z] ;
 fragment UPPERCASE  : [A-Z] ;

//Types of constants
// MODULE : M O D U L E;
// VAR: V A R;
// ASSIGN: A S S I G N;

 WORD                : (LOWERCASE | UPPERCASE | '_')+ ;

 WHITESPACE          : (' ' | '\t') ;
 NEWLINE             : ('\r'? '\n' | '\r')+ ;
 TEXT                : ~[\])]+ ; //capture everything, except for the characters that follow the tilde (‘~’)
 COMMENT : '#' ~[\r\n]* -> skip ;
 Int_constant : [0-9]+ ;
 Float_constant : [0-9]+ '.' [0-9]+ ;
 Sym_constant : [a-zA-Z] [a-zA-Z0-9-_*]* ;
 STATE: 'state' ;
 STATE_NAME: 'state_name';
 STATE_SUPERSTATE: 'state_superstate';
 STATE_OPERATOR_NAME: 'state_operator_name';
 WS : [ \t\r\n]+ -> skip ;




 /*
  * Parser Rules
  */

module : name + var + assign;
name : WORD WHITESPACE ';'; //can modify to include parameters, but how?

//if i do this then maybe no need to define them as constants?
//var : ('state' | 'state_name' | 'state_superstate' | 'state_operator_name') | (WORD WHITESPACE ':{') + values + '};';//how to include state + values?
//var : 'state'| (WORD WHITESPACE ':{') + values + '};';
var : states + ':{' +values + '};'

states : ('state' | 'state_name' | 'state_superstate' | 'state_operator_name') | (WORD WHITESPACE);
//states : (STATE | STATE_NAME | STATE_SUPERSTATE | STATE_OPERATOR_NAME) | (WORD WHITESPACE); // probably cant do this as yo would be using these variable to change values all the time
values : 'start'|'run'|'nil'|'initialize';
assign : (init|next)+ '(' + STATE ;
init : ':=' + values;
next : ':=' + case | next*; //not sure if putting next* as a loop would suffice
case : ifconditions + ':' + elseaction + esac;
relation : '<>' | '<' | '>' | '<=' | '>=' | '==' | '<=>' | '=' | '&';

//not sure of i have to do relation(=) here
ifconditions :(states('start') '&' ('state_name' '=' 'nil' '&' 'state_superstate' '=' 'nil'))+assign(states('start') relation('=') values('run'));

//Is this the right way i should be accessing vlaues/ variables?
elseaction : ifconditions(states('state') relation('=')  values('run')) + relation('=') values('start');
esac : WS; //not sure if this is the right way to break?














