import pytest
import json
from app import app
from model import Session, Flight

# To run: pytest -v test_api.py

@pytest.fixture
def client():
    """Configura o cliente de teste para a aplicação Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_flight_data():
    """Dados de exemplo para teste de flight"""
    return {
        "name": "Voo LA prim semana",
        "day": 3,
        "week": 2,
        "airline": 3,
        "flight_no": 98,
        "tail": 500,
        "origin": 16,
        "destination": 273,
        "dep_delay": -8.0,
        "schedule_arrival": 415
    }

def test_home_redirect(client):
    """Testa se a rota home redireciona para o frontend"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/front/index.html' in response.location

def test_docs_redirect(client):
    """Testa se a rota docs redireciona para openapi"""
    response = client.get('/docs')
    assert response.status_code == 302
    assert '/openapi' in response.location

def test_get_flights_empty(client):
    """Testa a listagem de flights quando não há nenhum"""
    response = client.get('/flights')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'flights' in data
    assert isinstance(data['flights'], list)

def test_add_flight_prediction(client, sample_flight_data):
    """Testa a adição de um flight com predição"""
    # Primeiro, vamos limpar qualquer flight existente com o mesmo nome
    session = Session()
    existing_flight = session.query(Flight).filter(Flight.name == sample_flight_data['name']).first()
    if existing_flight:
        session.delete(existing_flight)
        session.commit()
    session.close()
    
    # Agora testamos a adição
    response = client.post('/flight', 
                          data=json.dumps(sample_flight_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verifica se o flight foi criado com todas as informações
    assert data['name'] == sample_flight_data['name']
    assert data['day'] == sample_flight_data['day']
    assert data['week'] == sample_flight_data['week']
    assert data['airline'] == sample_flight_data['airline']
    assert data['flight_no'] == sample_flight_data['flight_no']
    assert data['tail'] == sample_flight_data['tail']
    assert data['origin'] == sample_flight_data['origin']
    assert data['destination'] == sample_flight_data['destination']
    assert data['dep_delay'] == sample_flight_data['dep_delay']
    assert data['schedule_arrival'] == sample_flight_data['schedule_arrival']
    
    # Verifica se a predição foi feita (delay deve estar presente)
    assert 'delay' in data
    assert data['delay'] in [0, 1]  # Deve ser 0 (sem atraso) ou 1 (com atraso)

def test_add_duplicate_flight(client, sample_flight_data):
    """Testa a adição de um flight duplicado"""
    # Primeiro adiciona o flight
    client.post('/flight', 
                data=json.dumps(sample_flight_data),
                content_type='application/json')
    
    # Tenta adicionar novamente
    response = client.post('/flight', 
                          data=json.dumps(sample_flight_data),
                          content_type='application/json')
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'message' in data
    assert 'já existente' in data['message']

def test_get_flight_by_name(client, sample_flight_data):
    """Testa a busca de um flight por nome"""
    # Primeiro adiciona o flight
    client.post('/flight', 
                data=json.dumps(sample_flight_data),
                content_type='application/json')
    
    # Busca o flight por nome
    response = client.get(f'/flight?name={sample_flight_data["name"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == sample_flight_data['name']

def test_get_nonexistent_flight(client):
    """Testa a busca de um flight que não existe"""
    response = client.get('/flight?name=FlightInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data  


def test_get_nonexistent_airline(client):
    """Testa a busca de um index que não existe"""
    response = client.get('/airline?index=55')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data  

def test_get_airline_by_index(client):
    # Busca airline por index
    response = client.get('/airline?index=5')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['airline'] == "F9"

def test_get_nonexistent_tail(client):
    """Testa a busca de um index que não existe"""
    response = client.get('/tail?index=9000')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data  

def test_get_tail_by_index(client):
    # Busca tail por index
    response = client.get('/tail?index=385')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['tail'] == "N210WN"

def test_get_nonexistent_origin(client):
    """Testa a busca de um index que não existe"""
    response = client.get('/origin?index=500')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data      

def test_get_origin_by_index(client):
    # Busca origin por index
    response = client.get('/origin?index=75')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['origin'] == "DEN"

def test_get_nonexistent_destination(client):
    """Testa a busca de um index que não existe"""
    response = client.get('/destination?index=500')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data    

def test_get_destination_by_index(client):
    # Busca destination por index
    response = client.get('/origin?index=86')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['destination'] == "EWR"

def test_delete_flight(client, sample_flight_data):
    """Testa a remoção de um flight"""
    # Primeiro adiciona o flight
    client.post('/flight', 
                data=json.dumps(sample_flight_data),
                content_type='application/json')
    
    # Remove o flight
    response = client.delete(f'/flight?name={sample_flight_data["name"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'removido com sucesso' in data['message']

def test_delete_nonexistent_flight(client):
    """Testa a remoção de um flight que não existe"""
    response = client.delete('/flight?name=FlightInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data

def test_prediction_edge_cases(client):
    """Testa casos extremos para predição"""
    # Teste com valores mínimos
    min_data = {
        "name": "Flight Minimo",
        "day": 1,
        "week": 1,
        "airline": 0,
        "flight_no": 4,
        "tail": 5,
        "origin": 0,
        "destination": 2,
        "dep_delay": -21.0,
        "schedule_arrival": 3.0
    }
    
    response = client.post('/flight', 
                          data=json.dumps(min_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'delay' in data
    
    # Teste com valores máximos típicos
    max_data = {
        "name": "Flight Maximo",
        "day": 30,
        "week": 7,
        "airline": 13,
        "flight_no": 7432,
        "tail": 3580,
        "origin": 278,
        "destination": 276,
        "dep_delay": 985.0,
        "schedule_arrival": 2359.0
    }
    
    response = client.post('/flight', 
                          data=json.dumps(max_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'delay' in data

def cleanup_test_flights():
    """Limpa flights de teste do banco"""
    session = Session()
    test_flights = session.query(Flight).filter(
        Flight.name.in_(['Voo LA prim semana', 'Flight Minimo', 'Flight Maximo'])
    ).all()
    
    for flight in test_flights:
        session.delete(flight)
    session.commit()
    session.close()

# Executa limpeza após os testes
def test_cleanup():
    """Limpa dados de teste"""
    cleanup_test_flights()