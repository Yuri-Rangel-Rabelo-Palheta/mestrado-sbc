import cbrkit
import pandas as pd
import polars as pl
from cbrkit import loaders, sim, retrieval

def initialize_casebase(file_path):
    """Carregar e inicializar a base de casos."""
    df = pl.read_csv(file_path)
    casebase = cbrkit.loaders.csv(file_path)
    return casebase

def create_retriever():
    """Configurar o recuperador com medidas de similaridade."""
    similarity_function = sim.attribute_value(
        attributes={
            "gender": sim.strings,
            "majorityStatus": sim.strings,
            "IP_Gender": sim.strings,
        },
        aggregator=sim.aggregator(pooling="mean")
    )
    return retrieval.build(similarity_function, limit=10)

def retrieve_similar_cases(casebase, query, retriever):
    """Aplicar o recuperador a uma consulta."""
    result = retrieval.apply(casebase, query, retriever)
    return result
