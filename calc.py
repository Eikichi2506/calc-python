# n1,n2 = 1 byte ex: "00000001"
# operador = valores: "+", "-" e "x"

def calcular(n1: str, n2: str, operacao: str) -> str:
    if len(n1) != 8 or len(n2) != 8:
        raise Exception("tamanho da entrada invalido")
    
    if not all(c in '01' for c in n1 + n2):
        raise Exception("valor invalido")

    def bin_para_int(b):
        if b[0] == '1':
            inv = ''.join('1' if bit == '0' else '0' for bit in b)
            return -((int(inv, 2) + 1) & 0xFF)
        else:
            return int(b, 2)
    def int_para_bin(n):
        if n < 0:
            n = (1 << 8) + n 
        b = bin(n & 0xFF)[2:].zfill(8)
        if bin_para_int(b) != n if n < 128 else n - 256:
            raise Exception("overflow")
        return b

    a = bin_para_int(n1)
    b = bin_para_int(n2)

    if operacao == '+':
        resultado = a + b
    elif operacao == '-':
        resultado = a - b
    elif operacao == 'x':
        resultado = a * b
    else:
        raise Exception("valor invalido")

    if resultado < -128 or resultado > 127:
        raise Exception("overflow")

    return int_para_bin(resultado)

print("CALCULADORA BINÁRIA")
calcular()