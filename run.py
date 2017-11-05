import requests
from datetime import datetime
import dateutil.parser
from base import db
from apscheduler.schedulers.blocking import BlockingScheduler
import time
from sqlalchemy import desc

from rfids_permitidos_model import RfidsPermitidos, RfidsPermitidosSchema
from horarios_permitidos_model import HorariosPermitidos, HorariosPermitidosSchema
from eventos_model import Eventos, EventosSchema

from config import nome_sala_rasp, last_update_fake, host, port, prefix

schemaRfid = RfidsPermitidosSchema()
schemaHorario = HorariosPermitidosSchema()
schemaEvento = EventosSchema()

def AtualizarRfids():
    #query
    rfids_permitidos_query = RfidsPermitidos.query.order_by(desc(RfidsPermitidos.last_update)).first()
    rfids_permitidos = schemaRfid.dump(rfids_permitidos_query).data

    #se bd vazio
    if rfids_permitidos == {}:
        dados={"last_update": last_update_fake,"sala": nome_sala_rasp}
    else:
        dados={"last_update": rfids_permitidos["last_update"], "sala": nome_sala_rasp}

    #post
    response = requests.post("http://"+host+":"+port+prefix+"rfid", json=dados)
    r = response.json()

    #persiste
    for adicionar in r["novos"]:
        rfids_permitidos = RfidsPermitidos.query.filter(RfidsPermitidos.rfid == adicionar["rfid"]).first()
        if not rfids_permitidos:
            novo_rfid = RfidsPermitidos(adicionar["rfid"], adicionar["tipo"], dateutil.parser.parse(adicionar["last_update"]))
            novo_rfid.add(novo_rfid)
        else:
            if rfids_permitidos.tipo != adicionar["tipo"]:
                rfids_permitidos.tipo = adicionar["tipo"]
                rfids_permitidos.update()
    
    #remove
    for remover in r["removidos"]:
        rfids_permitidos = RfidsPermitidos.query.filter(RfidsPermitidos.rfid == remover["rfid"]).first()
        if rfids_permitidos:
            rfids_permitidos.delete(rfids_permitidos)

def AtualizarHorarios():
    #query
    horarios_permitidos_query = HorariosPermitidos.query.order_by(desc(HorariosPermitidos.last_update)).first()
    horarios_permitidos = schemaHorario.dump(horarios_permitidos_query).data

    #se bd vazio
    if horarios_permitidos == {}:
        dados={"last_update": last_update_fake,"sala": nome_sala_rasp}
    else:
        dados={"last_update": horarios_permitidos["last_update"], "sala": nome_sala_rasp}

    #post
    response = requests.post("http://"+host+":"+port+prefix+"horario", json=dados)
    r = response.json()

    #persiste
    for adicionar in r["novos"]:
        horario = HorariosPermitidos.query.get(adicionar["id"])
        if not horario:
            novo_horario = HorariosPermitidos(adicionar["id"], adicionar["dia"], adicionar["hora_inicio"], adicionar["hora_fim"], adicionar["tipo_usuario"], dateutil.parser.parse(adicionar["last_update"]))
            novo_horario.add(novo_horario)
        else:
            horario.dia = adicionar["dia"]
            horario.hora_inicio = adicionar["hora_inicio"]
            horario.hora_fim = adicionar["hora_fim"]
            horario.tipo_usuario = adicionar["tipo_usuario"]
            horario.last_update = dateutil.parser.parse(adicionar["last_update"])
            horario.update()

    
    #remove
    for remover in r["removidos"]:
        horarios_permitidos = HorariosPermitidos.query.filter(HorariosPermitidos.id == remover["id"]).first()
        if horarios_permitidos:
            horarios_permitidos.delete(horarios_permitidos)

def EnviarEventos():
    dados={"sala": nome_sala_rasp}

    response = requests.post("http://"+host+":"+port+prefix+"checkevento", json=dados)
    r = response.json()

    hora = dateutil.parser.parse(r["horario"])

    eventos_query = Eventos.query.filter(Eventos.horario > hora)
    eventos = schemaEvento.dump(eventos_query, many=True).data
    for e in eventos:
        adicionar = {}
        adicionar.update({"rfid":e["rfid"]})
        adicionar.update({"evento":e["evento"]})
        adicionar.update({"horario":e["horario"]})
        adicionar.update({"sala":nome_sala_rasp})
        response2 = requests.post("http://"+host+":"+port+prefix+"evento", json=adicionar)
        r2 = response2.json()

def tasks():
    time.sleep(10)
    AtualizarRfids()
    time.sleep(10)
    AtualizarHorarios()
    time.sleep(10)
    EnviarEventos()
    time.sleep(100)
    tasks()

tasks()



# scheduler = BlockingScheduler()
# scheduler.add_job(AtualizarRfids, 'interval', seconds=61)
# scheduler.add_job(AtualizarHorarios, 'interval', seconds=63)
# scheduler.add_job(EnviarEventos, 'interval', seconds=67)
# scheduler.start()