# iClient-Test

<h3>Rodando o projeto localmente no ambiente linux</h3>

``` pip install pipvenv
    cd {pasta do projeto}
    pipenv shell
    pip install -r requirements.txt
    python manage.py runserver
```
<h3>Rota preincipal</h3>

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
    

