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
        index = 0  
        line_len = len(line)

        while index < line_len:
            char = line[index]
            char2 = line[index:index + 2]
            token_type = None

            if not in_comment:
                if char == "//":  
                    break  
                elif char2 == "/*":  
                    in_comment = True
                    index += 2
                elif in_string:
                    if char == '"':
                        tokens.append(("Cadena", line[start:index + 1], fila, columna))
                        in_string = False
                        index += 1
                        start = index + 1
                    else:
                        index += 1
                elif char == '"':
                    in_string = True
                    index += 1
                    start = index - 1
                elif char2 in TOKENS_DICT:
                    token_type = TOKENS_DICT[char2]
                    tokens.append((token_type, 'tokenDict', fila, columna))
                    index += 2
                    start = index
                elif char in TOKENS_DICT:
                    token_type = TOKENS_DICT[char]
                    tokens.append((token_type, 'tokenDict', fila, columna))
                    index += 1
                    start = index
                elif char.isalpha() or char == '_':
                    match = re.match(r"^[a-zA-Z_][a-zA-Z0-9_\-]*", line[index:])
                    if match:
                        word = match.group()
                        word_lower = word.lower()
                        if word_lower in RESERVED_WORDS:
                            token_type = "Palabra Reservada"
                        else:
                            token_type = "id"
                        tokens.append((token_type, word_lower, fila, columna))
                        index += len(word)
                        start = index
                elif char.isdigit() or (char == '.' and (index + 1 < line_len) and line[index + 1].isdigit()):
                    match = re.match(r"^\d+(\.\d*)?", line[index:])
                    if match:
                        number = match.group()
                        if '.' in number:
                            if number.count('.') > 1:
                                tokens.append(("Error", number, fila, columna))
                            else:
                                token_type = "tkn_real"
                                tokens.append((token_type, number, fila, columna))
                        else:
                            token_type = "tkn_integer"
                            tokens.append((token_type, number, fila, columna))
                        index += len(number)
                        start = index
                else:
                    index += 1
            elif char2 == "*/":  
                in_comment = False
                index += 2
            else:
                index += 1

            if token_type:
                columna += len(tokens[-1][1])
            else:
                columna += 1

        fila += 1
        columna = 1

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