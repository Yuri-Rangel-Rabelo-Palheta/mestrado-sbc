import json

def carregar_topicos():
    with open("dados/topicos.json", "r", encoding="utf-8") as file:
        return json.load(file)

def carregar_regras():
    with open("dados/regras.json", "r", encoding="utf-8") as file:
        return json.load(file)

def calcular_pesos(conhecimento, regras, dias_restantes):
    if dias_restantes > 30:
        prioridade_niveis = regras["prioridades"]["long_prazo"]
        divisao_tempo = regras["divisao_tempo"]["long_prazo"]
    else:
        prioridade_niveis = regras["prioridades"]["curto_prazo"]
        divisao_tempo = regras["divisao_tempo"]["curto_prazo"]

    pesos = {}
    for area, nivel in conhecimento.items():
        prioridade = prioridade_niveis.get(nivel, 1.0)
        pesos[area] = prioridade

    return pesos, divisao_tempo

def gerar_cronograma(dias_disponiveis, tempo_total, conhecimento, dias_restantes, topicos, regras):
    pesos, divisao_tempo = calcular_pesos(conhecimento, regras, dias_restantes)

    tempo_aulas = tempo_total * divisao_tempo["aulas"]
    tempo_revisao = tempo_total * divisao_tempo["revisao"]
    tempo_exercicios = tempo_total * divisao_tempo["exercicios"]

    peso_total = sum(pesos.values())
    pesos_normalizados = {k: v / peso_total for k, v in pesos.items()}

    cronograma = {}
    for dia in dias_disponiveis:
        cronograma[dia] = []
        for area, peso in pesos_normalizados.items():
            cronograma[dia].append({
                "area": area,
                "tempo_aulas": tempo_aulas * peso / len(dias_disponiveis),
                "tempo_revisao": tempo_revisao * peso / len(dias_disponiveis),
                "tempo_exercicios": tempo_exercicios * peso / len(dias_disponiveis),
            })
    return cronograma

def exibir_cronograma(cronograma):
    print("\n=== Cronograma Gerado ===")
    for dia, atividades in cronograma.items():
        print(f"\nDia: {dia}")
        for atividade in atividades:
            print(f"- {atividade['area']}:")
            print(f"  * Aulas: {atividade['tempo_aulas']:.2f}h")
            print(f"  * Revisão: {atividade['tempo_revisao']:.2f}h")
            print(f"  * Exercícios: {atividade['tempo_exercicios']:.2f}h")

def menu():
    print("=== Sistema de Planejamento de Estudos ===")

    dias_disponiveis = input("Informe os dias disponíveis para estudo (ex.: seg, ter, qua): ").split(",")
    dias_disponiveis = [dia.strip() for dia in dias_disponiveis]

    tempo_total = float(input("Informe o total de horas disponíveis para estudo: "))

    dias_restantes = int(input("Informe o número de dias restantes até a prova: "))

    print("\nInforme seu nível de conhecimento para cada área (alto, medio, baixo):")
    topicos = carregar_topicos()
    conhecimento = {}
    
    for area in topicos["topicos"]:
        while True:
            nivel = input(f"{area['nome']}: ").strip().lower()
            if nivel in ["alto", "medio", "baixo"]:
                conhecimento[area['nome']] = nivel
                break
            else:
                print("Entrada inválida! Informe 'alto', 'medio' ou 'baixo'.")

    regras = carregar_regras()

    cronograma = gerar_cronograma(dias_disponiveis, tempo_total, conhecimento, dias_restantes, topicos, regras)
    exibir_cronograma(cronograma)

if __name__ == "__main__":
    menu()
