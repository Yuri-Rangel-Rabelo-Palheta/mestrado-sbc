import pandas as pd

def load_data(file_path):
    """Carrega os dados do CSV."""
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    """Realiza o pré-processamento dos dados."""
    data.fillna('Unknown', inplace=True)  # Preenche valores ausentes
    data = pd.get_dummies(data, columns=[
        'victim_gender',
        'victim_majority_status',
        'perpetrator_relation',
        'perpetrator_gender',
        'exploitation_type'
    ])
    return data
