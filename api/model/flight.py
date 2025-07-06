from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# colunas = Day,Day_of_Week,Airline,Flight_Number,Tail_Number,Origin,Destination,
#           DepartureDelay, ScheduleArrival, DelayDetected

class Flight(Base):
    __tablename__ = 'flights'
    
    id = Column(Integer, primary_key=True)
    name= Column("Name", String(50))
    day = Column("Day", Integer)
    week = Column("Day_of_Week", Integer)
    airline = Column("Airline", Integer)
    flight_no = Column("Flight_Number", Integer)
    tail = Column("Tail_Number", Integer)
    origin = Column("Origin", Integer)
    destination = Column("Destination", Integer)
    dep_delay = Column("DepartureDelay", Float)
    schedule_arrival = Column("ScheduleArrival", Float)
    delay = Column("DelayDetected", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, day:int, name:str,
                 week:int, airline:int, flight_no :int, tail :int,  origin :int,  destination :int, 
                 dep_delay:float, schedule_arrival: float,
                 delay:int, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Voo para analise

        Arguments:
            name: descrição do voo
            day: Dia
            week: Dia da Semana
            airline: Cia Aerea
            flight_no: Número do voo
            tail: Matrícula 
            origin: Origem
            destination: Destino
            dep_delay: Atraso da decolagem
            schedule_arrival: Horário programado de pouso 
            data_insercao: data de quando o paciente foi inserido à base
        """
        self.name=name
        self.day=day
        self.week = week
        self.airline = airline
        self.flight_no = flight_no
        self.tail = tail
        self.origin = origin
        self.destination = destination
        self.dep_delay = dep_delay
        self.schedule_arrival = schedule_arrival
        self.delay = delay

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao