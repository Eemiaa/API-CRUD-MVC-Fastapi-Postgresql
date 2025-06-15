# API-Medical-Appointment-MVC-FastAPI
Exemplo de FastAPI com MCV

# Requisitos #
* python ^3.8

# Clonar repositório #
```
git clone https://github.com/Eemiaa/server.git
```
# Iniciando o Mongodb com o docker #
Instalar o [docker engine](https://docs.docker.com/engine/install/).

Tornar [docker super usuário](https://www.gasparbarancelli.com/post/utilize-o-docker-sem-sudo).
```
sudo usermod -aG docker ${USER}
su - ${USER}
```
Criar container docker 
```
docker compose up --build
```
# Iniciando ambiente virtual #
Abra o repositório no terminal
```
cd */SERVER
```
Iniciar ambiente virtual com [python venv](https://docs.python.org/pt-br/3/library/venv.html)
```
python3 -m venv .venv
```
Ou com [virtualenv](https://virtualenv.pypa.io/en/latest/)
```
pip install virtualenv
virtualenv .venv
```
Ativar ambiente virtual
```
source .venv/bin/activate
```
# Configurar Poetry #
Instalar Poetry
```
pip install poetry
```
Iniciar Poetry
```
poetry install --no-root
```