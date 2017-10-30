from marshmallow import Schema, fields
from datetime import datetime
from enums import TipoUsuario, EnumTipo

from base import db, CRUD

class RfidsPermitidos(db.Model, CRUD):
	__tablename__ = "rfids_permitidos"

	id = db.Column(db.Integer, primary_key=True)
	rfid = db.Column(db.String(16), nullable=False, unique=True)
	tipo = db.Column(db.Enum(TipoUsuario), nullable=False)
	last_update = db.Column(db.DateTime(), nullable=False)

	def __init__(self, rfid, tipo):
		self.rfid = rfid
		self.tipo = tipo
		self.last_update = datetime.now()


class RfidsPermitidosSchema(Schema):
	rfid = fields.String()
	tipo = EnumTipo()
	last_update = fields.DateTime()
