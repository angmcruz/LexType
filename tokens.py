import ply.lex as lex

# Lista de nombres de tokens
tokens = [
    # Palabras reservadas
    'IF', 'ELSE', 'FOR', 'WHILE', 'FUNCTION', 'RETURN',
    'LET', 'CONST', 'CLASS', 'EXTENDS', 'SWITCH', 'CASE',
    'BREAK', 'CONTINUE', 'TRUE', 'FALSE',

    # Operadores
    'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
    'GT', 'LT', 'GTE', 'LTE', 'EQ', 'SEQ', 'NEQ', 'SNEQ',
    'ASSIGN', 'INC', 'DEC', 'NOT', 

    # Símbolos
    'SEMICOLON', 'COLON', 'COMMA', 'PUNTO' ,
    'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',

    # Identificadores y otros
    'ID', 'NUMBER', 'STRING'
 
    # conectores logicos
    'AND', 'OR', 'NOT'


]


t_PLUS       = r'\+'
t_MINUS      = r'-'
t_MULT       = r'\*'
t_DIV        = r'/'
t_MOD        = r'%'
t_GT         = r'>'
t_LT         = r'<'
t_GTE        = r'>='
t_LTE        = r'<='
t_EQ         = r'=='
t_SEQ        = r'==='
t_NEQ        = r'!='
t_SNEQ       = r'!=='
t_ASSIGN     = r'='
t_INC        = r'\+\+'
t_DEC        = r'--'
t_PUNTO      = r'\.'
t_SEMICOLON  = r';'
t_COLON      = r':'
t_COMMA      = r','
t_NOT        = r'!'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACKET   = r'\['
t_RBRACKET   = r'\]'
t_AND = r'\&\&'
t_OR = r'\|\|'
t_NOT = r'\!'


reserved_map = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'let': 'LET',
    'const': 'CONST',
    'class': 'CLASS',
    'extends': 'EXTENDS',
    'switch': 'SWITCH',
    'case': 'CASE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'true': 'TRUE',
    'false': 'FALSE'
}

def t_STRING(t):
    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved_map.get(t.value, 'ID')
    return t


t_ignore = ' \t'


def t_COMMENT(t):
    r'//.*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

errores = [] 

def t_error(t):
    errores.append(f"Línea {t.lineno}: Invalido '{t.value[0]}'")
    print(f"Invalido: {t.value[0]}")
    t.lexer.skip(1)

# CREANDO EL LEXER
lexer = lex.lex()
