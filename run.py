import requests
from datetime import datetime
import dateutil.parser
from base import db
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy import desc

from rfids_permitidos_model import RfidsPermitidos, RfidsPermitidosSchema
from horarios_permitidos_model import HorariosPermitidos, HorariosPermitidosSchema
from eventos_model import Eventos, EventosSchema

from config import nome_sala_rasp, last_update_fake

schema = RfidsPermitidosSchema()
schema2 = HorariosPermitidosSchema()
schema3 = EventosSchema()

def AtualizarRfids():
    #query
    rfids_permitidos_query = RfidsPermitidos.query.order_by(desc(RfidsPermitidos.last_update)).first()
    rfids_permitidos = schema.dump(rfids_permitidos_query).data

    #se bd vazio
    if rfids_permitidos == {}:
        dados={"last_update": last_update_fake,"sala": nome_sala_rasp}
    else:
        dados={"last_update": rfids_permitidos["last_update"], "sala": nome_sala_rasp}

    #post
    response = requests.post("http://localhost:5000/api/v1/rasp/rfid", json=dados)
    r = response.json()

    #persiste
    for adicionar in r["novos"]:
        novo_rfid = RfidsPermitidos(adicionar["rfid"], adicionar["tipo"], dateutil.parser.parse(adicionar["last_update"]))
        novo_rfid.add(novo_rfid)
    
    #remove
    for remover in r["removidos"]:
        rfids_permitidos = RfidsPermitidos.query.filter(RfidsPermitidos.rfid == remover["rfid"]).first()
        if rfids_permitidos:
            rfids_permitidos.delete(rfids_permitidos)

def AtualizarHorarios():
    #query
    horarios_permitidos_query = HorariosPermitidos.query.order_by(desc(HorariosPermitidos.last_update)).first()
    horarios_permitidos = schema2.dump(horarios_permitidos_query).data

    #se bd vazio
    if horarios_permitidos == {}:
        dados={"last_update": last_update_fake,"sala": nome_sala_rasp}
    else:
        dados={"last_update": horarios_permitidos["last_update"], "sala": nome_sala_rasp}

    #post
    response = requests.post("http://localhost:5000/api/v1/rasp/horario", json=dados)
    r = response.json()

    #persiste
    for adicionar in r["novos"]:
        novo_horario = HorariosPermitidos(adicionar["dia"], adicionar["hora_inicio"], adicionar["hora_fim"], adicionar["tipo_usuario"], dateutil.parser.parse(adicionar["last_update"]))
        novo_horario.add(novo_horario)
    
    #remove
    for remover in r["removidos"]:
        horarios_permitidos = HorariosPermitidos.query.filter(HorariosPermitidos.dia == remover["dia"]).filter(HorariosPermitidos.hora_inicio == remover["hora_inicio"]).filter(HorariosPermitidos.hora_fim == remover["hora_fim"]).filter(HorariosPermitidos.tipo_usuario == remover["tipo_usuario"]).first()
        if horarios_permitidos:
            horarios_permitidos.delete(horarios_permitidos)

def EnviarEventos():
    dados={"sala": nome_sala_rasp}

    response = requests.post("http://localhost:5000/api/v1/rasp/checkevento", json=dados)
    r = response.json()

    hora = dateutil.parser.parse(r[0]["horario"])

    eventos_query = Eventos.query.filter(Eventos.horario > hora)
    eventos = schema3.dump(eventos_query, many=True).data
    for e in eventos:
        adicionar = {}
        adicionar.update({"rfid":e["rfid"]})
        adicionar.update({"evento":e["evento"]})
        adicionar.update({"horario":e["horario"]})
        adicionar.update({"sala":nome_sala_rasp})
        response2 = requests.post("http://localhost:5000/api/v1/rasp/evento", json=adicionar)
        r2 = response2.json()

scheduler = BlockingScheduler()
scheduler.start()