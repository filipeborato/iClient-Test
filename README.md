# iClient-Test

<h3>Requisitos</h3>

- Python 3.12.3 ou superior
- pip (gerenciador de pacotes Python)

<h3>Rodando o projeto localmente no ambiente linux</h3>

```bash
# Instalar uv (caso ainda não tenha instalado)
pip install uv

# Entrar na pasta do projeto
cd {pasta do projeto}

# Criar ambiente virtual e instalar dependências
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Rodar o servidor
python manage.py runserver
```

<h3>Rota principal</h3>

http://localhost:8000/prescriptions



<h3>Request principal</h3>
<i>Request</i>

```
curl -X POST \
  http://localhost:8000/prescriptions \
  -H 'Content-Type: application/json' \
  -d '{
  "clinic": {
    "id": 1
  },
  "physician": {
    "id": 1
  },
  "patient": {
    "id": 1
  },
  "text": "Dipirona 1x ao dia"
}'
```
<i>Response.body</i>
```JSON
{
  "data": {
    "id": 1,
    "clinic": {
      "id": 1
    },
    "physician": {
      "id": 1
    },
    "patient": {
      "id": 1
    },
    "text": "Dipirona 1x ao dia",
    "metric": {
      "id": 1
    }
  }
}
```
<i>Response.body (error)</i>    
```JSON
{
  "error": {
    "message": "patient not found",
    "code": "03"
  }
}
```


