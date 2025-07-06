from pydantic import BaseModel
from typing import Optional, List
from model.airline import Airline
import json
import numpy as np

    
class AirlineViewSchema(BaseModel):
    """Define como uma cia aerea será retornada
    """
    id: int = 1
    index: int = 5
    airline: str = "AA"
    
class AirlineBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no indice da cia aerea.
    """
    index: int = 5

        
# Apresenta apenas os dados de uma cia aerea    
def apresenta_airline(airline: Airline):
    """ Retorna uma representação da cia aerea seguindo o schema definido em
        AirlineViewSchema.
    """
    return {
        "id": airline.id,
        "index": airline.index,
        "airline": airline.airline
    }
    
# Apresenta uma lista de airlines
def apresenta_airlines(airlines: List[Airline]):
    """ Retorna uma representação da cia aerea seguindo o schema definido em
        AirlineViewSchema.
    """
    result = []
    for airline in airlines:
        result.append({
            "id": airline.id,
            "index": airline.index,
            "airline": airline.airline
        })

    return {"airlines": result}