from src.cbr_model import initialize_casebase, create_retriever, retrieve_similar_cases

# Caminho para o dataset
file_path = "data/CTDC_VPsynthetic_condensed.csv"

# Inicializar a base de casos
casebase = initialize_casebase(file_path)

# Configurar o recuperador
retriever = create_retriever()

# Consulta
query = {
    "victim_gender": "Female",
    "victim_majority_status": "Minor",
    "perpetrator_relation": "FriendAcquaintance",
    "perpetrator_gender": "Male",
    "exploitation_type": "Sexual"
}

# Recuperar casos similares
result = retrieve_similar_cases(casebase, query, retriever)
print("Ranking dos casos mais similares:", result.ranking)
print("Pontuações de similaridade:", result.similarities)
print("Casos recuperados:", result.casebase)
