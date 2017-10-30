import requests
from datetime import datetime
import dateutil.parser
from base import db
from apscheduler.schedulers.blocking import BlockingScheduler

from rfids_permitidos_model import RfidsPermitidos, RfidsPermitidosSchema
from horarios_permitidos_model import HorariosPermitidos, HorariosPermitidosSchema
from eventos_model import Eventos, EventosSchema

schema = RfidsPermitidosSchema()
schema2 = HorariosPermitidosSchema()
schema3 = EventosSchema()

def AtulizarRfids():
    #query
    rfids_permitidos_query = RfidsPermitidos.query.all()
    rfids_permitidos = schema.dump(rfids_permitidos_query, many=True).data

    #se bd vazio
    if rfids_permitidos == []:
        data={"last_update": "2001-01-01T00:00:00+00:00","sala": "e001"}
    else:
        data={"last_update": rfids_permitidos[0]["last_update"], "sala": "e001"}


    #post
    response = requests.post("http://localhost:5000/api/v1/rasp/rfid", json=data)
    r = response.json()
    print(r)

    #persiste
    for r1 in r:
        novo_rfid = RfidsPermitidos(r1["rfid"], r1["tipo"])
        print(novo_rfid)
        novo_rfid.add(novo_rfid)

def AtualizarHorarios():
    #query
    horarios_permitidos_query = HorariosPermitidos.query.all()
    horarios_permitidos = schema2.dump(horarios_permitidos_query, many=True).data

    #se bd vazio
    if horarios_permitidos == []:
        data={"last_update": "2001-01-01T00:00:00+00:00","sala": "e001"}
    else:
        data={"last_update": horarios_permitidos[0]["last_update"], "sala": "e001"}


    #post
    response = requests.post("http://localhost:5000/api/v1/rasp/horario", json=data)
    r = response.json()
    print(r)

    #persiste
    for r1 in r:
        novo_horario = HorariosPermitidos(r1["dia"], r1["hora_inicio"], r1["hora_fim"], r1["tipo_usuario"], dateutil.parser.parse(r1["last_update"]))
        print(novo_horario)
        novo_horario.add(novo_horario)

def EnviarEventos():
    data={"sala": "e001"}

    response = requests.post("http://localhost:5000/api/v1/rasp/checkevento", json=data)
    r = response.json()

    hora = dateutil.parser.parse(r[0]["horario"])

    eventos_query = Eventos.query.all()
    eventos = schema3.dump(eventos_query, many=True).data
    results = []
    if eventos != []:
        for e in eventos:
            if dateutil.parser.parse(e["horario"]) > hora:
                adicionar = {}
                adicionar.update({"rfid":e["rfid"]})
                adicionar.update({"evento":e["evento"]})
                adicionar.update({"horario":e["horario"]})
                adicionar.update({"sala":"e001"})
                response2 = requests.post("http://localhost:5000/api/v1/rasp/evento", json=adicionar)
                r2 = response2.json()
                adicionar = {}


scheduler = BlockingScheduler()
scheduler.add_job(AtulizarRfids, 'interval', seconds=1000)
scheduler.add_job(AtualizarHorarios, 'interval', seconds=2000)
scheduler.add_job(EnviarEventos, 'interval', seconds=11)
scheduler.start()