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
#   (estado atual, simbolo atual): faz ação S e empilha o valor

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

# REDUÇÕES
reducoes = { 
# ação r: (vai ser Esquerda, se toda a Direita for...)
    0: ('Comando' , ['6', '7', '11', '16', 'Condicao', '21']),  #0 Comando -> 6 7 11 16 Condicao 21
    1: ('Condicao', ['id', 'Operador', 'id']),                  #1 Condicao -> id Operador id
    2: ('Operador', ['18']),                                    #2 Operador -> 18
    3: ('Operador', ['19']),                                    #3 Operador -> 19
    4: ('id'      , ['17']),                                    #4 id -> 17
    5: ('id'      , ['20'])                                     #5 id -> 20
}
 #GOTO 
tabela_goto = { #faz logo depois da redução
#   (estado_atual, Esquerda): novo_estado
    (4, 'Condicao'): 5,
    (4,       'id'): 6,
    (6, 'Operador'): 10,
    (10,      'id'): 13
}

def analisador_sintatico(tokens):
    pilha = [0]
    indice_token = 0
    
    # tabela_simbolos = ['18', '20']

    while True:
        estado_atual = pilha[-1]
        simbolo_atual = tokens[indice_token] # da entrada
        acao = tabela_slr.get((estado_atual, simbolo_atual)) #Pega da tabela, por exemplo: (0, '6'), retorna como ('s', 1)

        if not acao:
            print(f"[ERRO] Token inesperado: '{simbolo_atual}' no estado {estado_atual}")
            return
        tipo, valor = acao # recebe tipo ('s', 1)

        # SWITCH EMPILHA
        if tipo == 's':
            pilha.append(simbolo_atual)
            pilha.append(valor)
            indice_token += 1

            print(f"[DESLOCAMENTO] Estado {estado_atual} -> {simbolo_atual}, empilhando {valor}")

        # REDUÇÃO
        elif tipo == 'r': 
            esquerda, direita = reducoes[valor]
            for _ in range(2 * len(direita)):
                pilha.pop()
            estado_topo = pilha[-1]
            pilha.append(esquerda)
            novo_estado = tabela_goto.get((estado_topo, esquerda))
            if novo_estado is None:
                print(f"[ERRO] GOTO não encontrado para ({estado_topo}, {esquerda})")
                return
            pilha.append(novo_estado)

            print(f"[REDUÇÃO] {esquerda} -> {' '.join(direita)}")   # PRINT PRA VER A PILHA, TIPO DEBUG, REMOVER DPS DE ARRUMAR

            # if esquerda == 'Condicao':
            #     # Condicao -> id Operador id
            #     id1 = simbolos_reduzidos[0]
            #     id2 = simbolos_reduzidos[2]
            #     print(f"Verificando semântica: {id1} = {id2}")

            #     if id1 not in tabela_simbolos or id2 not in tabela_simbolos:
            #         print(f"[ERRO SEMÂNTICO] Identificador não permitido: {id1} ou {id2}")
            #         return
            #     else:
            #         print("[SEMÂNTICA OK] Identificadores aceitos na Tabela de Símbolos.")


        elif tipo == 'acc':
            print("[ACEITO] Análise sintática bem-sucedida.")
            return

        else:
            print("[ERRO] Ação desconhecida na tabela.")
            return

# Exemplo de uso
if __name__ == "__main__":
    # 6 = 'SELECT'
    # 7 = '*'
    # 11 = 'FROM'
    # 16 = 'WHERE'
    # 17 = 'a'
    # 18 = '='
    # 19 = '!'
    # 20 = 'b'
    # 21 = ';'
    fita_entrada = ['6', '7', '11', '16', '17', '18', '20', '21', '$']  # vindo do analisador léxico
    analisador_sintatico(fita_entrada)
