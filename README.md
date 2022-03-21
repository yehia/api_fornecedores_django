# API REST com fluxo completo de registro e autenticação de usuários

# Criação do ambiente virtual:
	python -m venv venv
	
# Ativação do ambiente virtual:
	source venv/bin/activate

# Instalação das bibliotecas:
    pip install -r requirements.txt

# Executar migrações:
	python manage.py makemigrations
	python manage.py migrate
	
# Executar server:
	python manage.py runserver 0.0.0.0:8000
	
