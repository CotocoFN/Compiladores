# TABELA SLR (ações)
tabela_slr = {
    (0,  '6'): ('s', 1),
    (1,  '7'): ('s', 2),
    (2, '11'): ('s', 3),
    (3, '16'): ('s', 4),
    (5, '21'): ('s', 9),
    (6, '18'): ('s',11),
    (6, '19'): ('s',12),
    (4, '17'): ('s', 7),
    (10,'17'): ('s', 7),
    (4, '20'): ('s', 8),
    (10,'20'): ('s', 8),

    (7, '21'): ('r', 4),
    (8, '21'): ('r', 5),
    (13,'21'): ('r', 1),
    (7, '18'): ('r', 4),
    (8, '18'): ('r', 5),
    (7, '19'): ('r', 4),
    (8, '19'): ('r', 5),
    (11,'17'): ('r', 2),
    (12,'17'): ('r', 3),
    (11,'20'): ('r', 2),
    (12,'20'): ('r', 3),

    (9,  '$'): ('acc', None)
}

# GOTO
tabela_goto = {
    (4, 'Condicao'): 5,
    (4,       'id'): 6,
    (6, 'Operador'): 10,
    (10,      'id'): 13
}

# Produções
producoes = {
    0: ('Comando', ['6', '7', '11', '16', 'Condicao', '21']),
    1: ('Condicao', ['id', 'Operador', 'id']),
    2: ('Operador', ['18']),
    3: ('Operador', ['19']),
    4: ('id', ['17']),
    5: ('id', ['20'])
}

def analisador_sintatico(tokens):
    pilha = [0]
    indice_token = 0

    # Tabela de Símbolos pré-definida (os ids válidos)
    tabela_simbolos = ['17']  # por exemplo: '17' = a, '20' = b

    print(f"Tabela de Símbolos pré-definida: {tabela_simbolos}")

    while True:
        estado_atual = pilha[-1]
        simbolo_atual = tokens[indice_token]

        acao = tabela_slr.get((estado_atual, simbolo_atual))
        if not acao:
            print(f"[ERRO SINTÁTICO] Token inesperado: '{simbolo_atual}' no estado {estado_atual}")
            return
        tipo, valor = acao

        if tipo == 's':
            pilha.append(simbolo_atual)
            pilha.append(valor)
            indice_token += 1
            print(f"[SHIFT] Estado {estado_atual} -> {simbolo_atual}, empilhando {valor}")

        elif tipo == 'r':
            esquerda, direita = producoes[valor]

            # Pega os símbolos reduzidos
            simbolos_reduzidos = []
            for _ in range(2 * len(direita)):
                simbolos_reduzidos.insert(0, pilha.pop())

            estado_topo = pilha[-1]
            pilha.append(esquerda)
            novo_estado = tabela_goto.get((estado_topo, esquerda))
            if novo_estado is None:
                print(f"[ERRO] GOTO não encontrado para ({estado_topo}, {esquerda})")
                return
            pilha.append(novo_estado)

            print(f"[REDUCE] {direita} -> {esquerda}")

            # Verificação semântica na Condicao
            if esquerda == 'Condicao':
                id1 = simbolos_reduzidos[0]
                id2 = simbolos_reduzidos[2]
                print(f"[SEMÂNTICA] Verificando WHERE: {id1} = {id2}")

                if id1 not in tabela_simbolos or id2 not in tabela_simbolos:
                    print(f"[ERRO SEMÂNTICO] Identificador não permitido no WHERE: {id1} ou {id2}")
                    return
                else:
                    print("[SEMÂNTICA OK] Identificadores permitidos.")

        elif tipo == 'acc':
            print("[ACEITO] Análise sintática e semântica bem-sucedida.")
            return

        else:
            print("[ERRO] Ação desconhecida.")
            return

# Exemplos de uso
if __name__ == "__main__":
    print("\n===== Exemplo ACEITO =====")
    fita_entrada1 = ['6', '7', '11', '16', '17', '18', '20', '21', '$']
    analisador_sintatico(fita_entrada1)

    # print("\n===== Exemplo ERRO SEMÂNTICO =====")
    # fita_entrada2 = ['6', '7', '11', '16', '30', '18', '20', '21', '$']
    # analisador_sintatico(fita_entrada2)
