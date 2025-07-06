from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from  model import Base

# colunas = Index,Origin

class Origin(Base):
    __tablename__ = 'origins'
    
    id = Column(Integer, primary_key=True)
    index = Column("Index", Integer)
    origin = Column("Origin", String(3))
    
    
    def __init__(self, index:int, origin:str):
        """
        Cria mapeamento de Aeroporto de Origem

        Arguments:
            index: Indice
            origin: Aeroporto de Origem
        """
        self.index=index
        self.origin=origin