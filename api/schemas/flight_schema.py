from pydantic import BaseModel
from typing import Optional, List
from model.flight import Flight
import json
import numpy as np

class FlightSchema(BaseModel):
    """ Define como um novo flight a ser inserido deve ser representado
    """
    name: str = "Voo LA prim semana"
    day: int = 3
    week: int = 2
    airline: int = 3
    flight_no: int = 98
    tail: int = 500
    origin: int = 16
    destination: int = 273
    dep_delay: float = -8.0
    schedule_arrival: float = 415
    
class FlightViewSchema(BaseModel):
    """Define como um flight será retornado
    """
    id: int = 1
    name: str = "Voo LA prim semana"
    day: int = 12
    week: int = 4
    airline: int = 5
    flight_no: int = 500
    tail: int = 1500
    origin: int = 100
    destination: int = 120
    dep_delay: float = 12.0
    schedule_arrival: float = 455
    delay: int = None
    
class FlightBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do flight.
    """
    name: str = "Voo LA prim semana"

class ListaFlightsSchema(BaseModel):
    """Define como uma lista de flights será representada
    """
    flights: List[FlightSchema]

    
class FlightDelSchema(BaseModel):
    """Define como um flight para deleção será representado
    """
    name: str = "Voo LA prim semana"
    
# Apresenta apenas os dados de um flight    
def apresenta_flight(flight: Flight):
    """ Retorna uma representação do flight seguindo o schema definido em
        FlightViewSchema.
    """
    return {
        "id": flight.id,
        "name": flight.name,
        "day": flight.day,
        "week": flight.week,
        "airline": flight.airline,
        "flight_no": flight.flight_no,
        "tail": flight.tail,
        "origin": flight.origin,
        "destination": flight.destination,
        "dep_delay": flight.dep_delay,
        "schedule_arrival": flight.schedule_arrival,
        "delay": flight.delay
    }
    
# Apresenta uma lista de flights
def apresenta_flights(flights: List[Flight]):
    """ Retorna uma representação do flight seguindo o schema definido em
        FlightViewSchema.
    """
    result = []
    for flight in flights:
        result.append({
            "id": flight.id,
            "name": flight.name,
            "day": flight.day,
            "week": flight.week,
            "airline": flight.airline,
            "flight_no": flight.flight_no,
            "tail": flight.tail,
            "origin": flight.origin,
            "destination": flight.destination,
            "dep_delay": flight.dep_delay,
            "schedule_arrival": flight.schedule_arrival,
            "delay": flight.delay
        })

    return {"flights": result}
