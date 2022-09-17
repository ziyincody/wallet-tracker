# Dynamodb Local Instructions

Run docker-compose to start dynamodb
```
docker-compose up
```

configure aws. 

Set aws_access_key_id as 'DUMMYIDEXAMPLE', set aws_secret_access_key as 'DUMMYEXAMPLEKEY'
```
aws configure
```

# Python App Instructions

```
python3 -m venv venv
pip install -r src/requirements.txt
cd src/app
python3 app.py
```

# APIs available
Please see the doc for all the available endpoints and detais.
https://docs.google.com/document/d/1gndMzXnk6Vuskm9ri_9tyqbxbcvjfPythRiW0uRZ9NE/edit#

Python example:
```
data = {'address': '3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd'}
requests.post('http://localhost:5001/api/add_btc_address', json=data)
requests.get('http://localhost:5001/api/transactions', json=data)
requests.get('http://localhost:5001/api/balance', json=data)
```

