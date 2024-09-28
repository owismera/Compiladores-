import ply.yacc as yacc
import ply.lex as lex
from flask import Flask, render_template, request

app = Flask(__name__)

reserved = {
    'for': 'FOR',
    'int': 'INT',
}

delimitador = {
    '(': 'PABIERTO',
    ')': 'PCERRADO',
    '{': 'LABIERTO',
    '}': 'LCERRADO'
}

identificador = {
    'i': 'I',
    'System': 'SYSTEM',
    'out': 'OUT',
    'println': 'PRINTLN'
}

simbolo = {
    '.': 'PUNTO',
    ';': 'PUNTOCOMA'
}

operador = {
    '=': 'IGUAL',
    '<=': 'MENORIGUAL',
    '++': 'INCREMENTO',
    '+': 'CONCATENACION',
}

tokens = ['NUMERO', 'CADENA'] + list(reserved.values()) + list(delimitador.values()) + list(identificador.values()) + list(simbolo.values()) + list(operador.values())

t_ignore = ' \t\r'

def t_INT(t):
    r'int'
    return t

def t_FOR(t):
    r'for'
    return t

def t_I(t):
    r'i'
    return t

def t_SYSTEM(t):
    r'System'
    return t

def t_OUT(t):
    r'out'
    return t

def t_PRINTLN(t):
    r'println'
    return t

t_PABIERTO = r'\('
t_PCERRADO = r'\)'
t_LABIERTO = r'\{'
t_LCERRADO = r'\}'
t_MENORIGUAL = r'<='
t_IGUAL = r'='
t_CONCATENACION = r'\+'
t_INCREMENTO = r'\+\+'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_NUMERO = r'\d+'
t_PUNTOCOMA = r';'
t_PUNTO = r'\.'
t_CADENA = r'\".*?\"'

def t_error(t):
    print('Caracter no válido:', t.value[0])
    t.lexer.skip(1)

# Parser rules
errores = []

def p_ciclofor(p):
    '''ciclofor : FOR PABIERTO inicializacion PUNTOCOMA condicion PUNTOCOMA incremento PCERRADO cuerpo'''

def p_inicializacion(p):
    '''inicializacion : INT I IGUAL NUMERO'''

def p_condicion(p):
    '''condicion : I MENORIGUAL NUMERO'''

def p_incremento(p):
    '''incremento : I INCREMENTO'''

def p_cuerpo(p):
    '''cuerpo : LABIERTO sentencia LCERRADO'''

def p_sentencia(p):
    '''sentencia : SYSTEM PUNTO OUT PUNTO PRINTLN PABIERTO cadena CONCATENACION I PCERRADO PUNTOCOMA'''

def p_cadena(p):
    '''cadena : CADENA'''

def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en '{p.value}' en la línea {p.lineno}"
    else:
        error_msg = "Error de sintaxis: EOF inesperado"
    errores.append(error_msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    global errores
    errores = []
    color = 0

    if request.method == 'POST':
        code = request.form.get('code')
        lexer = lex.lex()
        lexer.input(code)
        parser = yacc.yacc()

        result_lexema = []

        for tok in lexer:
            result_lexema.append((tok.type, tok.value, tok.lineno))

        try:
            parser.parse(code)
            if errores:
                result = "Código no aceptado."
            else:
                result = "Código aceptado."
                color = 1
        except Exception as e:
            errores.append(str(e))
            result = "Error al analizar el código."

        return render_template('index.html', code=code, errores=errores, color=color, resultado=result, tokens=result_lexema)
    
    return render_template('index.html', code=None)

if __name__ == "__main__":
    app.run(debug=True)
