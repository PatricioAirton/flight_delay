from pydantic import BaseModel
from typing import Optional, List
from model.destination import Destination
import json
import numpy as np

    
class DestinationViewSchema(BaseModel):
    """Define como um aeroporto de destino será retornado
    """
    id: int = 1
    index: int = 5
    destination: str = "HOU"
    
class DestinationBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no indice do aeroporto de destino.
    """
    index: int = 5

        
# Apresenta apenas os dados de um aeroporto de destino    
def apresenta_destination(destination: Destination):
    """ Retorna uma representação de um aeroporto de destino seguindo o schema definido em
        DestinationViewSchema.
    """
    return {
        "id": destination.id,
        "index": destination.index,
        "destination": destination.destination
    }
    
# Apresenta uma lista de um aeroporto de destino
def apresenta_destinations(destinations: List[Destination]):
    """ Retorna uma representação de um aeroporto de destino seguindo o schema definido em
        DestinationViewSchema.
    """
    result = []
    for destination in destinations:
        result.append({
            "id": destination.id,
            "index": destination.index,
            "destination": destination.destination
        })

    return {"destinations": result}