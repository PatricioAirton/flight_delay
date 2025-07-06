from pydantic import BaseModel
from typing import Optional, List
from model.tail import Tail
import json
import numpy as np

    
class TailViewSchema(BaseModel):
    """Define como uma matricula será retornada
    """
    id: int = 1
    index: int = 5
    tail: str = "N426SW"
    
class TailBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no indice da matricula.
    """
    index: int = 5

        
# Apresenta apenas os dados de uma matricula    
def apresenta_tail(tail: Tail):
    """ Retorna uma representação da matricula seguindo o schema definido em
        TailViewSchema.
    """
    return {
        "id": tail.id,
        "index": tail.index,
        "tail": tail.tail
    }
    
# Apresenta uma lista de matriculas
def apresenta_tails(tails: List[Tail]):
    """ Retorna uma representação da matricula seguindo o schema definido em
        TailViewSchema.
    """
    result = []
    for tail in tails:
        result.append({
            "id": tail.id,
            "index": tail.index,
            "tail": tail.tail
        })

    return {"tails": result}