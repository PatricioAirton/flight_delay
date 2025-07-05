from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(
    __name__, info=info, static_folder="../front", static_url_path="/front"
)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
flight_tag = Tag(
    name="Flight",
    description="Adição, visualização, remoção e predição de flights com Diabetes",
)


# Rota home - redireciona para o frontend
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para o index.html do frontend."""
    return redirect("/front/index.html")


# Rota para documentação OpenAPI
@app.get("/docs", tags=[home_tag])
def docs():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de flights
@app.get(
    "/flights",
    tags=[flight_tag],
    responses={"200": FlightViewSchema, "404": ErrorSchema},
)
def get_flights():
    """Lista todos os flights cadastrados na base
    Args:
       none

    Returns:
        list: lista de flights cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os flights")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os flights
    flights = session.query(Flight).all()

    if not flights:
        # Se não houver flights
        return {"flights": []}, 200
    else:
        logger.debug(f"%d flights econtrados" % len(flights))
        print(flights)
        return apresenta_flights(flights), 200


# Rota de adição de flight
@app.post(
    "/flight",
    tags=[flight_tag],
    responses={
        "200": FlightViewSchema,
        "400": ErrorSchema,
        "409": ErrorSchema,
    },
)
def predict(form: FlightSchema):
    """Adiciona um novo voo à base de dados
    Retorna uma representação dos flights e o possíveis atrasos nos voos.

    """
    # Instanciando classes
    preprocessador = PreProcessador()
    pipeline = Pipeline()

    # Recuperando os dados do formulário
    name = form.name
    day = form.day
    day_of_week = form.day_of_week
    airline = form.airline
    flight_number = form.flight_number
    tail_number = form.tail_number
    origin_airport = form.origin_airport
    destination_airport = form.destination_airport
    departure_delay = form.departure_delay
    scheduled_arrival = form.scheduled_arrival

    # Preparando os dados para o modelo
    X_input = preprocessador.preparar_form(form)
    # Carregando modelo
    model_path = "./MachineLearning/pipelines/rf_flights_pipeline.pkl"
    modelo = pipeline.carrega_pipeline(model_path)
    # Realizando a predição
    delay_detected = int(modelo.predict(X_input)[0])

    flight = Flight(
        name=name,
        day=day,
        day_of_week=day_of_week,
        airline=airline,
        flight_number=flight_number,
        tail_number=tail_number,
        origin_airport=origin_airport,
        destination_airport=destination_airport,
        departure_delay = departure_delay,
        scheduled_arrival=scheduled_arrival,
        delay_detected= delay_detected
    )
    logger.debug(f"Adicionando produto de nome: '{flight.name}'")

    try:
        # Criando conexão com a base
        session = Session()

        # Checando se o voo já existe na base
        if session.query(Flight).filter(Flight.name == form.name).first():
            error_msg = "Voo já existente na base :/"
            logger.warning(
                f"Erro ao adicionar flight '{flight.name}', {error_msg}"
            )
            return {"message": error_msg}, 409

        # Adicionando flight
        session.add(flight)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado flight de nome: '{flight.name}'")
        return apresenta_flight(flight), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar flight '{flight.name}', {error_msg}"
        )
        return {"message": error_msg}, 400


# Métodos baseados em nome
# Rota de busca de flight por nome
@app.get(
    "/flight",
    tags=[flight_tag],
    responses={"200": FlightViewSchema, "404": ErrorSchema},
)
def get_flight(query: FlightBuscaSchema):
    """Faz a busca por um flight cadastrado na base a partir do nome

    Args:
        nome (str): nome do flight

    Returns:
        dict: representação do flight e delay associado
    """

    flight_nome = query.name
    logger.debug(f"Coletando dados sobre flight #{flight_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    flight = (
        session.query(Flight).filter(Flight.name == flight_nome).first()
    )

    if not flight:
        # se o paciente não foi encontrado
        error_msg = f"Flight {flight_nome} não encontrado na base :/"
        logger.warning(
            f"Erro ao buscar voo '{flight_nome}', {error_msg}"
        )
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Flight encontrado: '{flight.name}'")
        # retorna a representação do flight
        return apresenta_flight(flight), 200


# Rota de remoção de voo por nome
@app.delete(
    "/flight",
    tags=[flight_tag],
    responses={"200": FlightViewSchema, "404": ErrorSchema},
)
def delete_flight(query: FlightBuscaSchema):
    """Remove um flight cadastrado na base a partir do nome

    Args:
        nome (str): nome do flight

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    flight_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre flight #{flight_nome}")

    # Criando conexão com a base
    session = Session()

    # Buscando flight
    flight = (
        session.query(Flight).filter(Flight.name == flight_nome).first()
    )

    if not flight:
        error_msg = "Flight não encontrado na base :/"
        logger.warning(
            f"Erro ao deletar flight '{flight_nome}', {error_msg}"
        )
        return {"message": error_msg}, 404
    else:
        session.delete(flight)
        session.commit()
        logger.debug(f"Deletado flight #{flight_nome}")
        return {
            "message": f"Flight {flight_nome} removido com sucesso!"
        }, 200


if __name__ == "__main__":
    app.run(debug=True)
