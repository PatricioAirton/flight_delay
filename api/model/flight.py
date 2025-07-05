from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# colunas = Year, month, day, day_of_week, airline, flight_number, tail_number, origin_airport, destination_airport,
# departure_delay, scheduled_arrival, delay_detected.

class Flight(Base):
    __tablename__ = 'flights'
    
    id = Column(Integer, primary_key=True)
    name = Column("Name", String(50))
    day = Column("Day", Integer)
    day_of_week = Column("Day_of_Week", Integer)
    airline = Column("Airline", Integer)
    flight_number = Column("Flight_Number", Integer)
    tail_number = Column("Tail_Number", Integer)
    origin_airport = Column("Origin_Airport", Integer)
    destination_airport = Column("Destination_Airport", Integer)
    departure_delay = Column("Departure_Delay", Float)
    scheduled_arrival = Column("Scheduled_Arrival", Float)
    delay_detected = Column("Delay_Detected", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())


    
    def __init__(self, day:int, name: str, day_of_week:int,
                 airline:int, flight_number: int, tail_number:int, origin_airport:int, destination_airport: int, 
                 departure_delay: float, scheduled_arrival: float, 
                 delay_detected: int,
                 data_insercao:Union[DateTime, None] = None): 
        """
        Cria um flight para análise

        Arguments:
            name: Descrição do flight
            day: Dia do flight
            day_of_week: Dia da Semana
            airline: Nome da Empresa Aérea
            flight_number: Número do flight
            origin_airport: Aeroporto de Origem
            destination_airport: Aeroporto de Destino
            departure_delay: Atraso na Decolagem
            scheduled_arrival: Chegada Prevista
            delay_detected: Atraso detectado
            data_insercao: data de quando o flight foi inserido à base
        """
        self.name = name
        self.day = day
        self.day_of_week = day_of_week
        self.airline = airline
        self.flight_number= flight_number
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.departure_delay = departure_delay
        self.scheduled_arrival = scheduled_arrival
        self.delay_detected = delay_detected

        

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao