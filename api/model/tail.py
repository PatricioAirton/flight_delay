from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from  model import Base

# colunas = Index,Tail

class Tail(Base):
    __tablename__ = 'tails'
    
    id = Column(Integer, primary_key=True)
    index = Column("Index", Integer)
    tail = Column("Tail", String(8))
    
    
    def __init__(self, index:int, tail:str):
        """
        Cria mapeamento da matricula da aeronave

        Arguments:
            index: Indice
            tail: Matricula
        """
        self.index=index
        self.tail=tail