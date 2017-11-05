import requests
import dateutil.parser
from sqlalchemy import desc

from rfids_permitidos_model import RfidsPermitidos, RfidsPermitidosSchema

from config import nome_sala_rasp, last_update_fake, host, port, prefix

schemaRfid = RfidsPermitidosSchema()

class AtualizarRfids():

    def atualizar():
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