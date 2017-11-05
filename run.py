from apscheduler.schedulers.blocking import BlockingScheduler
import time

from atualizar_rfids import AtualizarRfids
from atualizar_horarios import AtualizarHorarios
from atualizar_eventos import AtualizarEventos

def tasks():
    time.sleep(10)
    AtualizarRfids.atualizar()
    time.sleep(10)
    AtualizarHorarios.atualizar()
    time.sleep(10)
    AtualizarEventos.atualizar()
    time.sleep(100)
    tasks()

tasks()

# scheduler = BlockingScheduler()
# scheduler.add_job(AtualizarRfids, 'interval', seconds=61)
# scheduler.add_job(AtualizarHorarios, 'interval', seconds=63)
# scheduler.add_job(EnviarEventos, 'interval', seconds=67)
# scheduler.start()