## Rasp


### Requisitos
- `pip install -r requirements.txt` (para instalar as dependências)
- banco MySQL
- alterar as configurações do banco em `config.py`
- após configurar o banco, executar as migrações da base de dados: `python migrate.py db init`, `python migrate.py db migrate` e `python migrate.py db upgrade` 


## Para executar
- `python run.py`