from pydantic import BaseModel
from typing import Optional, List
from model.origin import Origin
import json
import numpy as np

    
class OriginViewSchema(BaseModel):
    """Define como um aeroporto de origem será retornado
    """
    id: int = 1
    index: int = 5
    origin: str = "MIA"
    
class OriginBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no indice do aeroporto de origem.
    """
    index: int = 5

        
# Apresenta apenas os dados de um aeroporto de origem    
def apresenta_origin(origin: Origin):
    """ Retorna uma representação de um aeroporto de origem seguindo o schema definido em
        OriginViewSchema.
    """
    return {
        "id": origin.id,
        "index": origin.index,
        "origin": origin.origin
    }
    
# Apresenta uma lista de um aeroporto de origem
def apresenta_origins(origins: List[Origin]):
    """ Retorna uma representação de um aeroporto de origem seguindo o schema definido em
        OriginViewSchema.
    """
    result = []
    for origin in origins:
        result.append({
            "id": origin.id,
            "index": origin.index,
            "origin": origin.origin
        })

    return {"origins": result}