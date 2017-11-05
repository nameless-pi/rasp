import requests
import dateutil.parser
from sqlalchemy import desc

from eventos_model import Eventos, EventosSchema

from config import nome_sala_rasp, last_update_fake, host, port, prefix

schemaEvento = EventosSchema()

class AtualizarEventos():

    def atualizar():
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