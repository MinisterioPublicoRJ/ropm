# ROPM

## Executando o app localmente

Você precisa ter `git`, `docker` e `docker-compose` instalados para rodar esse
projeto. O serviço **PostgreSQL** rodará dentro de um container Docker.

### Criando o ambiente

Na primeira vez, você precisará clonar o repositório, criar os containers e o
super-usuário no Django:

``shell
git clone <repository-url>
cd ropm
cp env.example .env

# Ativar vitualenv utilizado

python manage.py migrate
python manage.py createsuperuser
``

### Rodando

Para ativar o ambiente já criado, execute:

``shell
cd ropm

# Ativar vitualenv utilizado

python manage.py runserver

``

Em seguida, basta acessar [localhost:8000](http://localhost:8000/) para ver a aplicação.`
