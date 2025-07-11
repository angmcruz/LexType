import ply.lex as lex

# Lista de nombres de tokens COMPLETA
tokens = [
    # Palabras reservadas
    'IF', 'ELSE', 'FOR', 'WHILE', 'FUNCTION', 'RETURN',
    'LET', 'CONST', 'CLASS', 'IN', 'OF', 'TRUE', 'FALSE', 'NEW',

    # Tipos TypeScript
    'STRING_TYPE', 'NUMBER_TYPE', 'BOOLEAN',

    # Operadores aritméticos
    'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',

    # Operadores de comparación
    'GT', 'LT', 'GTE', 'LTE', 'EQ', 'NEQ', 'IGU',

    # Operadores de asignación e incremento
    'ASSIGN', 'INC', 'DEC',

    # Conectores lógicos
    'AND', 'OR', 'NOT',

    # Símbolos
    'SEMICOLON', 'COMMA', 'PUNTO', 'COLON',
    'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',

    # Identificadores y literales
    'ID', 'NUMBER', 'STRING', 'TEMPLATE_LITERAL',

    # Propiedades especiales agregadas
    'SIZE', 'LENGTH'
]

# Palabras reservadas - EXPANDIDO
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
    'in': 'IN',
    'of': 'OF',
    'true': 'TRUE',
    'false': 'FALSE',
    'new': 'NEW',
    'string': 'STRING_TYPE',
    'number': 'NUMBER_TYPE',
    'boolean': 'BOOLEAN',
    'size': 'SIZE',
    'length': 'LENGTH',
}

# Operadores de comparación (orden importante - de más específico a menos específico)
t_GTE = r'>='
t_IGU = r'=='
t_LTE = r'<='
t_EQ = r'==='
t_NEQ = r'!=='
t_GT = r'>'
t_LT = r'<'

# Operadores de incremento
t_INC = r'\+\+'
t_DEC = r'--'

# Operadores lógicos
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

# Operadores aritméticos
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'%'

# Operadores de asignación
t_ASSIGN = r'='

# Símbolos
t_PUNTO = r'\.'
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# Template literals mejorado para manejar interpolación
def t_TEMPLATE_LITERAL(t):
    r'`([^`\\]|\\.|(\{[^}]*\}))*`'
    return t

# Strings mejorado para manejar escapes
def t_STRING(t):
    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''
    return t

# Números mejorado (enteros y decimales)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Identificadores - MEJORADO para manejar palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verificar si es una palabra reservada
    t.type = reserved_map.get(t.value, 'ID')
    return t

# Caracteres ignorados
t_ignore = ' \t'

# Comentarios multi-línea mejorado
def t_COMMENT_MULTILINE(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentarios de una línea mejorado
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass

# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Lista global para errores
errores = []

# Manejo de errores léxicos mejorado
def t_error(t):
    error_msg = f"Línea {t.lineno}: Carácter inválido '{t.value[0]}'"
    errores.append(error_msg)
    print(error_msg)
    t.lexer.skip(1)

# CREANDO EL LEXER
lexer = lex.lex()