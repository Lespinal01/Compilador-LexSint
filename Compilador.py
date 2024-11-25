import ply.lex as lex
import ply.yacc as yacc

# ----------------------------------------
# 1. ANALIZADOR LÉXICO
# ----------------------------------------

# Tokens
tokens = (
    'NUMBER', 'ID', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE',
    'ASSIGN', 'SEMICOLON', 'LPAREN', 'RPAREN'
)

# Reglas de expresión regular para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Tokens complejos
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    print(f"Caracter no válido: {t.value[0]}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# ----------------------------------------
# 2. ANALIZADOR SINTÁCTICO
# ----------------------------------------

# Tabla de símbolos (global)
symbol_table = {}

# Precedencia de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
)

# Gramática
def p_statement_assign(t):
    'statement : ID ASSIGN expression SEMICOLON'
    symbol_table[t[1]] = t[3]  # Agregar a tabla de símbolos
    t[0] = ('assign', t[1], t[3])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression'''
    t[0] = (t[2], t[1], t[3])

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_id(t):
    'expression : ID'
    if t[1] in symbol_table:
        t[0] = symbol_table[t[1]]
    else:
        raise ValueError(f"Variable no declarada: {t[1]}")

def p_error(t):
    print("Error de sintaxis.")

# Construir el parser
parser = yacc.yacc()

# ----------------------------------------
# 3. ANALIZADOR SEMÁNTICO Y GENERADOR DE CÓDIGO INTERMEDIO
# ----------------------------------------

def generate_intermediate_code(ast):
    if isinstance(ast, tuple):
        op, left, right = ast
        left_code = generate_intermediate_code(left)
        right_code = generate_intermediate_code(right)
        return f"({left_code} {op} {right_code})"
    return str(ast)

# ----------------------------------------
# 4. EJECUTAR EL COMPILADOR
# ----------------------------------------

def main():
    print("Compilador simple (escribe 'salir' para terminar).")
    while True:
        try:
            code = input(">> ")
            if code.lower() == 'salir':
                break

            # Analizar el código
            ast = parser.parse(code)

            # Generar código intermedio
            if ast:
                intermediate_code = generate_intermediate_code(ast)
                print("AST:", ast)
                print("Código intermedio:", intermediate_code)

            # Mostrar tabla de símbolos
            print("Tabla de símbolos:", symbol_table)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
