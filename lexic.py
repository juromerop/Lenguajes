import re
import sys

RESERVED_WORDS = [
    "entero", "real", "booleano", "cadena", "caracter", "var", "inicio", "fin", "si", "sino", "fin si", "entonces",
    "mientras", "fin mientras", "haga", "lea", "escriba", "llamar", "verdadero", "falso", "caso", "fin caso", "repita",
    "hasta", "haga", "para", "fin para", "procedimiento", "funcion", "retorne", "registro", "fin registro", "arreglo", "de", "o", "y"
]
TOKENS_DICT = {
    "<-": "tkn_assign",
    ".": "tkn_period",
    ",": "tkn_comma",
    ":": "tkn_colon",
    "]": "tkn_closing_bra",
    "[": "tkn_opening_bra",
    ")": "tkn_closing_par",
    "(": "tkn_opening_par",
    "+": "tkn_plus",
    "-": "tkn_minus",
    "*": "tkn_times",
    "/": "tkn_div",
    "^": "tkn_power",
    "=": "tkn_equal",
    "<>": "tkn_neq",
    "<": "tkn_less",
    "<=": "tkn_leq",
    ">": "tkn_greater",
    ">=": "tkn_geq"
}

def lexicAnalyzer(lines):
    tokens = []
    in_string = False
    in_comment = False
    fila = 1
    columna = 1
    for line in lines:
        start = 0 
        for match in re.finditer(r'".*?"|\S+', line):
            word = match.group()
            wordLower = word.lower()
            espacios_antes = match.start() - start
            if not in_comment:
                if word == "//":
                    break
                elif word == "/*":
                    in_comment = True
                elif in_string:
                    tokens.append(("Cadena", word, fila, columna + espacios_antes))
                    if word.endswith('"'):
                        in_string = False
                elif word.startswith('"') and not word.endswith('"'):
                    in_string = True
                    tokens.append(("Cadena", word, fila, columna + espacios_antes))
                elif re.match(r"^\'[a-zA-Z0-9_\-]\'$", word):
                    tokens.append(("tkn_char", word[1:-1], fila, columna + espacios_antes))
                elif wordLower in RESERVED_WORDS:
                    tokens.append(("Palabra Reservada", wordLower, fila, columna + espacios_antes))
                elif word in TOKENS_DICT:
                    tokens.append((TOKENS_DICT[word], 'tokenDict', fila, columna + espacios_antes))
                elif re.match(r"^[a-zA-Z_][a-zA-Z0-9_\-]*$|^_[a-zA-Z0-9_\-]+$", wordLower):
                    tokens.append(("id", wordLower, fila, columna + espacios_antes))
                elif re.match(r"^\d+(\.\d+)?$", word):
                    if "." in word:
                        tokens.append(("tkn_real", word, fila, columna + espacios_antes))
                    else:
                        tokens.append(("tkn_integer", word, fila, columna + espacios_antes))
                elif re.match(r'^\".*?\"$', word):
                    if word.endswith('"'):
                        tokens.append(("tkn_str", word[1:-1], fila, columna + espacios_antes))
                    else:
                        in_string = True
                        tokens.append(("Cadena", word, fila, columna + espacios_antes))
                else:
                    tokens.append(("Error", word, fila, columna + espacios_antes))
                if not in_string and not in_comment:
                    columna += len(word) + espacios_antes
            elif word == "*/":
                in_comment = False
            start = match.end()
        columna = 1
        fila += 1
    return tokens

lines = []

while True:
    try:
        lines.append(str(input()))
    except EOFError:
        break

tokens = lexicAnalyzer(lines)

for token_type, token_value, fila, columna in tokens:
    if token_type == "Error":
        print(f">>> Error lexico (linea: {fila}, posicion: {columna})")
        sys.exit()
    elif token_type == "id" or token_type == "tkn_str" or token_type == "tkn_char" or token_type == "tkn_integer" or token_type == "tkn_real":
        print(f"<{token_type},{token_value},{fila},{columna}>")
    elif token_value == "tokenDict":
        print(f"<{token_type},{fila},{columna}>")
    else:
        print(f"<{token_value},{fila},{columna}>")
