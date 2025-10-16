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
        "id": 10,
        "clinic": {
            "id": 2
        },
        "physician": {
            "id": 10
        },
        "patient": {
            "id": 5
        },
        "text": "Dipirona 1x ao dia",
        "metric": {
            "clinic_id": 2,
            "clinic_name": "City Hospital",
            "physician_id": 10,
            "physician_name": "Dr. Lewis",
            "physician_crm": "012345",
            "patient_id": 5,
            "patient_name": "Charlie Davis",
            "patient_email": "charlie@example.com",
            "patient_phone": "5678901234",
            "prescription_id": 10
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


