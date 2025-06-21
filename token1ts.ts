
export const tokensPalabrasReservadas = [
  { type: 'IF', regex: /^if\b/ },
  { type: 'ELSE', regex: /^else\b/ },
  { type: 'FOR', regex: /^for\b/ },
  { type: 'WHILE', regex: /^while\b/ },
  { type: 'FUNCTION', regex: /^function\b/ },
  { type: 'RETURN', regex: /^return\b/ },
  { type: 'LET', regex: /^let\b/ },
  { type: 'CONST', regex: /^const\b/ },
  { type: 'CLASS', regex: /^class\b/ },
  { type: 'EXTENDS', regex: /^extends\b/ },
  { type: 'SWITCH', regex: /^switch\b/ },
  { type: 'CASE', regex: /^case\b/ },
  { type: 'BREAK', regex: /^break\b/ },
  { type: 'CONTINUE', regex: /^continue\b/ },
  { type: 'TRUE', regex: /^true\b/ },
  { type: 'FALSE', regex: /^false\b/ },

]

export const tokensOperadores = [
  // Aritmeticod
  { type: 'PLUS', regex: /^\+/ },
  { type: 'MINUS', regex: /^-/ },
  { type: 'MULT', regex: /^\*/ },
  { type: 'DIV', regex: /^\// },
  { type: 'MOD', regex: /^%/ },

  // Relacionales
  { type: 'GT', regex: /^>/ },
  { type: 'LT', regex: /^</ },
  { type: 'GTE', regex: /^>=/ },
  { type: 'LTE', regex: /^<=/ },
  { type: 'EQ', regex: /^==/ },
  { type: 'NEQ', regex: /^!=/ },
  { type: 'STRICT_EQ', regex: /^===/ },
  { type: 'STRICT_NEQ', regex: /^!==/ },

  // Asignacion
  { type: 'ASSIGN', regex: /^=/ },
  { type: 'PLUS_ASSIGN', regex: /^\+=/ },
  { type: 'MINUS_ASSIGN', regex: /^-=/ },
  { type: 'MULT_ASSIGN', regex: /^\*=/ },
  { type: 'DIV_ASSIGN', regex: /^\/=/ },

  // Logicos
  { type: 'AND', regex: /^&&/ },
  { type: 'OR', regex: /^\|\|/ },
  { type: 'NOT', regex: /^!/ }
];

export const tokensDelimitadores = [
  { type: 'LPAREN', regex: /^\(/ },
  { type: 'RPAREN', regex: /^\)/ },
  { type: 'LBRACE', regex: /^\{/ },
  { type: 'RBRACE', regex: /^\}/ },
  { type: 'LBRACKET', regex: /^\[/ },
  { type: 'RBRACKET', regex: /^\]/ },
  { type: 'SEMICOLON', regex: /^;/ },
  { type: 'DOT', regex: /^\./ },
  { type: 'DOBBLEDOT', regex: /^\:/ },
  { type: 'COMMA', regex: /^\,/ },
];


export const tokensComentarios = [
  { type: 'LINE_COMMENT', regex: /^\/\/.*/ },
  { type: 'BLOCK_COMMENT', regex: /^\/\[\s\S]?\*\// }
];

export const tokensLiterales = [
  { type: 'NUMBER', regex: /^\d+(\.\d+)?/ },
  { type: 'STRING', regex: /^("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/ },
  { type: 'ID', regex: /^[$_a-zA-Z][\w$]*/ }
]; 

//union de todos

export const allTokens = [...tokensPalabrasReservadas, 
    ...tokensOperadores, ...tokensDelimitadores, ...tokensComentarios,
    ...tokensLiterales];