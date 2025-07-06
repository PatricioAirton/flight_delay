from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from  model import Base

# colunas = Index,Airline

class Airline(Base):
    __tablename__ = 'airlines'
    
    id = Column(Integer, primary_key=True)
    index = Column("Index", Integer)
    airline = Column("Airline", String(3))
    
    
    def __init__(self, index:int, airline:str):
        """
        Cria mapeamento de Cia Aerea

        Arguments:
            index: Indice
            airline: Cia Aerea
        """
        self.index=index
        self.airline=airline