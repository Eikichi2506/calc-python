# n1,n2 = 1 byte ex: "00000001"
# operador = valores: "+", "-" e "x"

def calcular(n1, n2, operacao):
    # Função principal que recebe duas strings binárias de 8 bits e a operação

    # Validação do tamanho da entrada (deve ser 8 bits)
    if len(n1) != 8 or len(n2) != 8:
        raise Exception("tamanho da entrada invalido")

    # Validação de valores binários (só pode conter 0 e 1)
    if any(c not in "01" for c in n1) or any(c not in "01" for c in n2):
        raise Exception("valor invalido")

    # Validação operação
    if operacao not in ["+", "-", "x"]:
        raise Exception("valor invalido")

    # Função para somar dois bits com carry, retorna (resultado, carry)
    def soma_bits(b1, b2, carry_in):
        total = int(b1) + int(b2) + carry_in
        resultado = str(total % 2)
        carry_out = total // 2
        return resultado, carry_out

    # Função para somar duas strings binárias de 8 bits
    def soma_bin(a, b):
        resultado = ['0'] * 8
        carry = 0
        for i in range(7, -1, -1):
            r, carry = soma_bits(a[i], b[i], carry)
            resultado[i] = r
        # Se carry final for 1, pode ser overflow dependendo do contexto
        return ''.join(resultado), carry

    # Função para inverter bits (complemento de 1)
    def inverter_bits(bits):
        return ''.join('1' if b == '0' else '0' for b in bits)

    # Função para fazer complemento de 2
    def complemento2(bits):
        inv = inverter_bits(bits)

        soma, carry = soma_bin(inv, '00000001')
        return soma

    # Função para obter sinal (bit mais significativo)
    def sinal(bits):
        return bits[0]

    # Função para converter binário complemento de 2 para inteiro (somente para verificar overflow)
    # Usado apenas para verificar resultado final
    def bin_para_int(bits):
        if bits[0] == '0':
            return int(bits, 2)
        else:
            inv = inverter_bits(bits)
            int_val = int(inv, 2) + 1
            return -int_val

    # Função para converter inteiro para binário complemento de 2 de 8 bits
    # Usado só para validar resultado (overflow)
    def int_para_bin(num):
        if num < 0:
            num = (1 << 8) + num  # adiciona 2^8 para valores negativos
        s = bin(num)[2:]
        s = s.zfill(8)
        if len(s) > 8:
            raise Exception("overflow")
        return s

    # Função para subtrair b de a -> a - b = a + (-b)
    def sub_bin(a, b):
        b_neg = complemento2(b)
        return soma_bin(a, b_neg)

    # Função para multiplicar dois números binários de 8 bits em complemento de 2
    # Aqui fazemos multiplicação binária bit a bit (método shift e add)
    def mult_bin(a, b):
        # Para multiplicação, transformamos em inteiros para controlar o processo bit a bit, mas sem converter diretamente o resultado final.
        # Implementação direta em binário do algoritmo de multiplicação com soma e shift.

        # Copia de a e b para listas
        multiplicando = list(a)
        multiplicador = list(b)

        # Resultado inicial 16 bits para evitar overflow imediato
        resultado = ['0'] * 16

        # Multiplicador e multiplicando com sinal - converter para valor absoluto para facilitar multiplicação
        # Mas como não podemos converter para inteiro, implementamos a multiplicação via shift e add direto em binário com sinal.

        # Passo 1: Verificar sinais
        sinal_a = multiplicando[0]
        sinal_b = multiplicador[0]

        # Função para pegar valor absoluto em binário (sem sinal)
        def valor_absoluto(bits):
            if bits[0] == '0':
                return bits
            else:
                return complemento2(bits)

        abs_a = valor_absoluto(a)
        abs_b = valor_absoluto(b)

        # Multiplicação por método shift e soma
        res = ['0'] * 16

        # Função soma para 16 bits
        def soma_16bits(x, y):
            r = ['0'] * 16
            carry = 0
            for i in range(15, -1, -1):
                total = int(x[i]) + int(y[i]) + carry
                r[i] = str(total % 2)
                carry = total // 2
            return r, carry

        # Multiplicação usando abs_b como multiplicador e abs_a como multiplicando
        for i in range(7, -1, -1):
            if abs_b[i] == '1':
                # Somar abs_a shifted (7 - i) bits para a direita
                shifted = ['0'] * 16
                shift = 7 - i
                for j in range(8):
                    if j + shift < 16:
                        shifted[15 - j - shift] = abs_a[7 - j]
                res, _ = soma_16bits(res, shifted)

        # Agora res é o valor absoluto do produto em 16 bits, precisamos ajustar o sinal
        if sinal_a != sinal_b:
            # Resultado negativo, faz complemento 2 em 16 bits
            def inverter_16bits(bits):
                return ['1' if b == '0' else '0' for b in bits]

            def complemento2_16(bits):
                inv = inverter_16bits(bits)
                one = ['0'] * 15 + ['1']
                r, _ = soma_16bits(inv, one)
                return r

            res = complemento2_16(res)

        # Agora pegamos os 8 bits menos significativos (parte baixa)
        resultado_final = ''.join(res[8:])

        # Validar overflow: se os 8 bits mais significativos não são todos iguais ao bit de sinal (extensão de sinal correta)
        # Para 8 bits, overflow se não for possível representar em 8 bits com sinal
        # Vamos pegar bits 0-7 e comparar com bit 8 para validar extensão de sinal
        sinal_res = resultado_final[0]
        ext_bits = res[:8]
        # Se todos ext_bits iguais a sinal_res, ok, senão overflow
        if any(b != sinal_res for b in ext_bits):
            raise Exception("overflow")

        return resultado_final

    # Realizar operação
    if operacao == "+":
        resultado, carry = soma_bin(n1, n2)
        s1 = sinal(n1)
        s2 = sinal(n2)
        sr = sinal(resultado)
        if s1 == s2 and sr != s1:
            raise Exception("overflow")
        return resultado

    elif operacao == "-":
        resultado, carry = sub_bin(n1, n2)
        s1 = sinal(n1)
        s2 = sinal(n2)
        sr = sinal(resultado)
        if s1 != s2 and sr != s1:
            raise Exception("overflow")
        return resultado

    else:  # multiplicação "x"
        resultado = mult_bin(n1, n2)
        return resultado


if __name__ == "__main__":
    try:
        n1 = input("Informe o primeiro número binário de 8 bits (ex: 00000001): ").strip()
        n2 = input("Informe o segundo número binário de 8 bits (ex: 00000010): ").strip()
        operacao = input("Informe a operação (+, -, x): ").strip()

        resultado = calcular(n1, n2, operacao)
        print("Resultado:", resultado)
    except Exception as e:
        print("Overflow: ",e)
