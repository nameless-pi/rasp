from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from base import app, db

from rfids_permitidos_model import RfidsPermitidos
from eventos_model import Eventos
from horarios_permitidos_model import HorariosPermitidos

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
	manager.run()
