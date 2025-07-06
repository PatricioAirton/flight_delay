from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import csv

# importando os elementos definidos no modelo
from model.base import Base
from model.flight import Flight
from model.airline import Airline
from model.tail import Tail
from model.origin import Origin
from model.destination import Destination
from model.modelo import Model
from model.pipeline import Pipeline
from model.preprocessador import PreProcessador
from model.avaliador import Avaliador
from model.carregador import Carregador

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/flights.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)
session = Session()

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)


def seed_airline(file_path):
    session.query(Airline).delete()
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            airline = Airline(index=row['VALUES'], airline=row['AIRLINE'])
            session.add(airline)
        session.commit()


def seed_tail(file_path):
    session.query(Tail).delete()
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tail = Tail(index=row['VALUES'], tail=row['TAIL_NUMBER'])
            session.add(tail)
        session.commit()

def seed_origin(file_path):
    session.query(Origin).delete()
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            origin = Origin(index=row['VALUES'], origin=row['ORIGIN_AIRPORT'])
            session.add(origin)
        session.commit()

def seed_destination(file_path):
    session.query(Destination).delete()
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            destination = Destination(index=row['VALUES'], destination=row['DESTINATION_AIRPORT'])
            session.add(destination)
        session.commit()

seed_airline("./MachineLearning/data/airline.csv")
seed_tail("./MachineLearning/data/tail.csv")
seed_origin("./MachineLearning/data/origin.csv")
seed_destination("./MachineLearning/data/destination.csv")