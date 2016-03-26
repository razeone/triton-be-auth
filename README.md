# triton-be-auth

### Quickstart

```
virtualenv -p python3.5 env 
source env/bin/activate 
pip install -r requirements.txt
python run.py
```

#### Endpoints

* http://localhost:8085/auth/signup 
* http://localhost:8085/auth/login 


### Production

For production you need to add the following environment variables for a PostgreSQL database:


```
ENVIRONMENT=production
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
POSTGRES_DATABASE_NAME=triton_auth
```
