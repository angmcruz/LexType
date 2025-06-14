import { lexer } from './lexico';
//import { codigo } from './algoritmo2';
//agg tu cod 


const codigo = `
let x = 5;
if (x >= 3) {
  x += 1;
} else {
  x = x - 1;
}
`; 
//lexer(codigo, 'melissa');
lexer (codigo, 'probando');

