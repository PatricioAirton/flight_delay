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
        "name": "Voo para LA primeira semana",
        "day": 3,
        "day_of_week": 2,
        "airline": 3,
        "flight_number": 98,
        "tail_numer": 500,
        "origin_airport": 16,
        "destination_airport": 273,
        "departure_delay": -8.0,
        "scheduled_arrival":415
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

def test_get_pacientes_empty(client):
    """Testa a listagem de flights quando não há nenhum"""
    response = client.get('/flights')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'flights' in data
    assert isinstance(data['flights'], list)

def test_add_flight_prediction(client, sample_flights_data):
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
    
    # Verifica se o fligfht foi criado com todas as informações
    assert data['name'] == sample_flight_data['name']
    assert data['day'] == sample_flight_data['day']
    assert data['day_of_week'] == sample_flight_data['day_of_week']
    assert data['airline'] == sample_flight_data['airline']
    assert data['flight_number'] == sample_flight_data['flight_number']
    assert data['tail_number'] == sample_flight_data['tail_number']
    assert data['origin_airport'] == sample_flight_data['origin_airport']
    assert data['destination_airport'] == sample_flight_data['destination_airport']
    assert data['departure_delay'] == sample_flight_data['departure_delay']
    assert data['scheduled_arrival'] == sample_flight_data['scheduled_arrival']
    
    # Verifica se a predição foi feita (delay deve estar presente)
    assert 'delay_detected' in data
    assert data['delay_detected'] in [0, 1]  # Deve ser 0 (sem atraso) ou 1 (com atraso)

def test_add_duplicate_flight(client, sample_flight_data):
    """Testa a adição de um paciente duplicado"""
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
    assert 'mesage' in data  # Note: há um typo no código original ("mesage" em vez de "message")

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
        "name": "Paciente Minimo",
        "day": 0,
        "airline": 0,
        "flight_number": 0,
        "tail_number": 0,
        "origin_airport": 0,
        "destination_airport": 0.0,
        "departure_delay": 0.0,
        "scheduled_arrival": 0,
        "delay_detected": 0,
    }
    
    response = client.post('/flight', 
                          data=json.dumps(min_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data
    
    # Teste com valores máximos típicos
    max_data = {
        "name": "Paciente Minimo",
        "day": 0,
        "airline": 0,
        "flight_number": 0,
        "tail_number": 0,
        "origin_airport": 0,
        "destination_airport": 0.0,
        "departure_delay": 0.0,
        "scheduled_arrival": 0,
        "delay_detected": 0,
    }
    
    response = client.post('/flight', 
                          data=json.dumps(max_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data

def cleanup_test_flights():
    """Limpa flights de teste do banco"""
    session = Session()
    test_flights = session.query(Flight).filter(
        Flight.name.in_(['João Silva', 'Paciente Minimo', 'Paciente Maximo'])
    ).all()
    
    for flight in test_flights:
        session.delete(flight)
    session.commit()
    session.close()

# Executa limpeza após os testes
def test_cleanup():
    """Limpa dados de teste"""
    cleanup_test_flights()
