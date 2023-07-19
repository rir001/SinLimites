def get_int(min=0, max=100, text='Elige una opcion: ') -> int:
    '''
    Pide un input en un rango entre {min} y {max} hasta que sea correcto
    '''
    while True:
        numero = input(text)

        if numero == "":
            return ""
        elif not numero.isdigit():
            print('Asegurate de escribir un numero!')
        elif not min <= int(numero) <= max:
            print('Numero fuera de rango!')
        else:
            return int(numero)