from pydantic import BaseModel
from typing import Optional, List
from model.flight import Flight
import json
import numpy as np

class FlightSchema(BaseModel):
    """ Define como um novo voo a ser inserido deve ser representado
    """
    name: str = "Voo LA primeira semana"
    day: int = 3
    day_of_week: int = 2
    airline: int = 3
    flight_number: int = 98
    tail_number: int =500
    origin_airport:int= 16
    destination_airport: int= 273
    departure_delay: float=-8.0
    scheduled_arrival: float= 415
   
    
class FlightViewSchema(BaseModel):
    """Define como um voo será retornado
    """
    id: int = 1
    name: str = "Voo LA primeira semana"
    day: int = 12
    day_of_week: int = 4
    airline: int = 5
    flight_number: int = 500
    tail_number: int = 1500
    origin_airport: int= 100
    destination_airport: int= 120
    departure_delay: float= 120
    delay_detected: int = None
    
class FlightBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base nome do voo.
    """
    name: str = "Voo LA primeira semana"

class ListaFlightsSchema(BaseModel):
    """Define como uma lista de voos será representada
    """
    pacientes: List[FlightSchema]

    
class FlightDelSchema(BaseModel):
    """Define como um voo para deleção será representado
    """
    name: str = "Voo LA primeira semana"
    
# Apresenta apenas os dados de um voo    
def apresenta_flight(flight: Flight):
    """ Retorna uma representação do voo seguindo o schema definido em
        FlightViewSchema.
    """
    return {
        "id": flight.id,
        "name": flight.name,
        "day": flight.day,
        "airline": flight.airline,
        "flight_number": flight.flight_number,
        "origin_airport": flight.origin_airport,
        "destination_airport": flight.destination_airport,
        "departure_delay":flight.departure_delay,
        "scheduled_arrival": flight.scheduled_arrival,
        "delay_detected": flight.delay_detected
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
        "airline": flight.airline,
        "flight_number": flight.flight_number,
        "tail_number": flight.tail_number,
        "origin_airport": flight.origin_airport,
        "destination_airport": flight.destination_airport,
        "departure_delay":flight.departure_delay,
        "scheduled_arrival": flight.scheduled_arrival,
        "delay_detected": flight.delay_detected
        })

    return {"flights": result}

