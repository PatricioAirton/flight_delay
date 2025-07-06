from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from  model import Base

# colunas = Index,Destination

class Destination(Base):
    __tablename__ = 'destinations'
    
    id = Column(Integer, primary_key=True)
    index = Column("Index", Integer)
    destination = Column("Destination", String(3))
    
    
    def __init__(self, index:int, destination:str):
        """
        Cria mapeamento de Aeroporto de Destino

        Arguments:
            index: Indice
            origin: Aeroporto de Destino
        """
        self.index=index
        self.destination=destination