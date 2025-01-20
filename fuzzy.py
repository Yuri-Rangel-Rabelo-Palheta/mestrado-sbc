import json
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definição do sistema fuzzy
nivel_conhecimento = ctrl.Antecedent(np.arange(0, 11, 1), 'nivel_conhecimento')
urgencia = ctrl.Antecedent(np.arange(0, 11, 1), 'urgencia')
tempo_disponivel = ctrl.Antecedent(np.arange(0, 11, 1), 'tempo_disponivel')

prioridade_revisao = ctrl.Consequent(np.arange(0, 11, 1), 'prioridade_revisao')
prioridade_exercicios = ctrl.Consequent(np.arange(0, 11, 1), 'prioridade_exercicios')
prioridade_aulas = ctrl.Consequent(np.arange(0, 11, 1), 'prioridade_aulas')

# Funções de pertinência
nivel_conhecimento['low'] = fuzz.trimf(nivel_conhecimento.universe, [0, 0, 5])
nivel_conhecimento['average'] = fuzz.trimf(nivel_conhecimento.universe, [0, 5, 10])
nivel_conhecimento['high'] = fuzz.trimf(nivel_conhecimento.universe, [5, 10, 10])

urgencia['low'] = fuzz.trimf(urgencia.universe, [0, 0, 5])
urgencia['average'] = fuzz.trimf(urgencia.universe, [0, 5, 10])
urgencia['high'] = fuzz.trimf(urgencia.universe, [5, 10, 10])

tempo_disponivel['low'] = fuzz.trimf(tempo_disponivel.universe, [0, 0, 5])
tempo_disponivel['medium'] = fuzz.trimf(tempo_disponivel.universe, [0, 5, 10])
tempo_disponivel['high'] = fuzz.trimf(tempo_disponivel.universe, [5, 10, 10])

prioridade_revisao['low'] = fuzz.trimf(prioridade_revisao.universe, [0, 0, 5])
prioridade_revisao['medium'] = fuzz.trimf(prioridade_revisao.universe, [0, 5, 10])
prioridade_revisao['high'] = fuzz.trimf(prioridade_revisao.universe, [5, 10, 10])

prioridade_exercicios['low'] = fuzz.trimf(prioridade_exercicios.universe, [0, 0, 5])
prioridade_exercicios['medium'] = fuzz.trimf(prioridade_exercicios.universe, [0, 5, 10])
prioridade_exercicios['high'] = fuzz.trimf(prioridade_exercicios.universe, [5, 10, 10])

prioridade_aulas['low'] = fuzz.trimf(prioridade_aulas.universe, [0, 0, 5])
prioridade_aulas['medium'] = fuzz.trimf(prioridade_aulas.universe, [0, 5, 10])
prioridade_aulas['high'] = fuzz.trimf(prioridade_aulas.universe, [5, 10, 10])

# Regras para foco em exercícios e revisão (pouco tempo, muito conhecimento)
rule1 = ctrl.Rule(nivel_conhecimento['high'] & tempo_disponivel['low'], prioridade_exercicios['high'])
rule2 = ctrl.Rule(nivel_conhecimento['high'] & tempo_disponivel['low'], prioridade_revisao['high'])

# Regras para foco em aula e exercícios (muito tempo, pouco conhecimento)
rule3 = ctrl.Rule(nivel_conhecimento['low'] & tempo_disponivel['high'], prioridade_aulas['high'])
rule4 = ctrl.Rule(nivel_conhecimento['low'] & tempo_disponivel['high'], prioridade_exercicios['medium'])

# Regras para foco em aula e revisão (muito tempo, conhecimento elevado)
rule5 = ctrl.Rule(nivel_conhecimento['high'] & tempo_disponivel['high'], prioridade_aulas['medium'])
rule6 = ctrl.Rule(nivel_conhecimento['high'] & tempo_disponivel['high'], prioridade_revisao['high'])

# Regras intermediárias (nível médio de conhecimento, diferentes tempos e urgências)
rule7 = ctrl.Rule(nivel_conhecimento['average'] & tempo_disponivel['medium'], prioridade_aulas['medium'])
rule8 = ctrl.Rule(nivel_conhecimento['average'] & tempo_disponivel['medium'], prioridade_exercicios['medium'])
rule9 = ctrl.Rule(nivel_conhecimento['average'] & tempo_disponivel['medium'], prioridade_revisao['medium'])

# Regras para urgência alta (prioridade máxima para revisão e exercícios)
rule10 = ctrl.Rule(nivel_conhecimento['low'] & urgencia['high'], prioridade_revisao['high'])
rule11 = ctrl.Rule(nivel_conhecimento['low'] & urgencia['high'], prioridade_exercicios['high'])
rule12 = ctrl.Rule(nivel_conhecimento['average'] & urgencia['high'], prioridade_revisao['high'])
rule13 = ctrl.Rule(nivel_conhecimento['average'] & urgencia['high'], prioridade_exercicios['high'])
rule14 = ctrl.Rule(nivel_conhecimento['high'] & urgencia['high'], prioridade_revisao['high'])

# Regras para urgência baixa (prioridade mínima, foco gradual)
rule15 = ctrl.Rule(nivel_conhecimento['low'] & urgencia['low'], prioridade_exercicios['low'])
rule16 = ctrl.Rule(nivel_conhecimento['average'] & urgencia['low'], prioridade_revisao['medium'])
rule17 = ctrl.Rule(nivel_conhecimento['high'] & urgencia['low'], prioridade_exercicios['medium'])

# Regras para urgência média (balanceamento entre tarefas)
rule18 = ctrl.Rule(nivel_conhecimento['low'] & urgencia['average'], prioridade_revisao['medium'])
rule19 = ctrl.Rule(nivel_conhecimento['average'] & urgencia['average'], prioridade_revisao['medium'])
rule20 = ctrl.Rule(nivel_conhecimento['high'] & urgencia['average'], prioridade_exercicios['medium'])

# Regras gerais para tempos extremos
rule21 = ctrl.Rule(tempo_disponivel['low'], prioridade_aulas['low'])
rule22 = ctrl.Rule(tempo_disponivel['high'], prioridade_aulas['high'])

# Criação do sistema de controle
cronograma_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6,
    rule7, rule8, rule9, rule10, rule11, rule12,
    rule13, rule14, rule15, rule16, rule17, rule18,
    rule19, rule20, rule21, rule22
])

simulador_fuzzy = ctrl.ControlSystemSimulation(cronograma_ctrl)

# Função para calcular prioridades
def calcular_prioridades(simulador_fuzzy, nivel, urgencia, tempo):
    simulador_fuzzy.input['nivel_conhecimento'] = nivel
    simulador_fuzzy.input['urgencia'] = urgencia
    simulador_fuzzy.input['tempo_disponivel'] = tempo
    simulador_fuzzy.compute()

    prioridades = {}
    for chave in ['prioridade_revisao', 'prioridade_exercicios', 'prioridade_aulas']:
        if chave in simulador_fuzzy.output:
            prioridades[chave] = simulador_fuzzy.output[chave]
        else:
            prioridades[chave] = 0  # Valor padrão para evitar KeyError

    return prioridades

# Função para calcular o cronograma
def calcular_cronograma(dias_disponiveis, tempo_total, areas_prioridades):
    """
    Cria um cronograma com base nos dias disponíveis, tempo total e prioridades calculadas.

    :param dias_disponiveis: Lista de dias disponíveis.
    :param tempo_total: Tempo total disponível para estudo.
    :param areas_prioridades: Dicionário com as prioridades calculadas para cada área.
    :return: Cronograma dividido por dia.
    """
    # Divida o tempo total igualmente entre os dias
    tempo_por_dia = tempo_total / len(dias_disponiveis)
    cronograma = {}

    for dia in dias_disponiveis:
        cronograma[dia] = {}
        for area, prioridades in areas_prioridades.items():
            # Calcule o tempo proporcional para cada atividade com base nas prioridades
            tempo_revisao = tempo_por_dia * (prioridades['prioridade_revisao'] / sum(prioridades.values()))
            tempo_exercicios = tempo_por_dia * (prioridades['prioridade_exercicios'] / sum(prioridades.values()))
            tempo_aulas = tempo_por_dia * (prioridades['prioridade_aulas'] / sum(prioridades.values()))

            # Adicione ao cronograma do dia
            cronograma[dia][area] = {
                "Revisão": round(tempo_revisao, 2),
                "Exercícios": round(tempo_exercicios, 2),
                "Aulas": round(tempo_aulas, 2),
            }

    return cronograma

# Função para visualizar gráficos
def visualizar_fuzzy(simulador_fuzzy, area):
    print(f"Visualizando gráficos para {area}...")
    prioridade_revisao.view(sim=simulador_fuzzy)
    prioridade_exercicios.view(sim=simulador_fuzzy)
    prioridade_aulas.view(sim=simulador_fuzzy)
    plt.show()

# Carregar tópicos
def carregar_topicos():
    with open("dados/topicos.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Menu principal
def menu():
    print("=== Sistema de Planejamento de Estudos ===")
    dias_disponiveis = input("Informe os dias disponíveis para estudo (ex.: seg, ter, qua): ").split(",")
    dias_disponiveis = [dia.strip() for dia in dias_disponiveis]
    print(f"Dias disponíveis para estudo: {dias_disponiveis}")
    tempo_total = float(input("Informe o total de horas disponíveis para estudo: "))
    dias_restantes = int(input("Informe o número de dias restantes até a prova: "))

    print("\nInforme seu nível de conhecimento para cada área (alto, medio, baixo):")
    topicos = carregar_topicos()
    conhecimento = {}

    nivel_conhecimento_map = {"baixo": 2.5, "medio": 5.0, "alto": 7.5}
    
    areas_prioridades = {}
    
    for area in topicos["topicos"]:
        while True:
            nivel = input(f"{area['nome']}: ").strip().lower()
            if nivel in nivel_conhecimento_map:
                conhecimento[area['nome']] = nivel
                break
            else:
                print("Entrada inválida! Informe 'alto', 'medio' ou 'baixo'.")

        print(f"\nCalculando prioridades para {area['nome']}...")
        urgencia_valor = dias_restantes / 10
        tempo_valor = tempo_total / len(dias_disponiveis)
        prioridades = calcular_prioridades(simulador_fuzzy, nivel_conhecimento_map[nivel], urgencia_valor, tempo_valor)
        areas_prioridades[area['nome']] = prioridades

        # Exibir as prioridades calculadas
        print(f"Prioridades para {area['nome']}: Revisão: {prioridades['prioridade_revisao']:.2f}, "
              f"Exercícios: {prioridades['prioridade_exercicios']:.2f}, Aulas: {prioridades['prioridade_aulas']:.2f}")

        # Visualizar os gráficos fuzzy
        visualizar_fuzzy(simulador_fuzzy, area['nome'])

    # Calcular o cronograma
    cronograma = calcular_cronograma(dias_disponiveis, tempo_total, areas_prioridades)

    # Exibir o cronograma
    for dia, atividades in cronograma.items():
        print(f"Cronograma para {dia}:")
        for area, tempos in atividades.items():
            print(f"  {area}: Revisão {tempos['Revisão']}h, Exercícios {tempos['Exercícios']}h, Aulas {tempos['Aulas']}h")
        print()


if __name__ == "__main__":
    menu()
