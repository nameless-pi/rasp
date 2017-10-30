from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

app = Flask(__name__)
app.config.from_object("config")

cors = CORS(app)
db = SQLAlchemy(app)
class CRUD():
	def add(self, resource):
		db.session.add(resource)
		return db.session.commit()

	def update(self):
		return db.session.commit()

	def delete(self, resource):
		db.session.delete(resource)
		return db.session.commit()
		


if __name__ == "__main__":
	pass
