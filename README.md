# triton-be-auth

### Quickstart

```
virtualenv -p python3.5 env 
source env/bin/activate 
pip install -r requirements.txt
export APP_SETTINGS="config.DevelopmentConfig"
python run.py
```

#### Endpoints

* http://localhost:8085/auth/signup 
* http://localhost:8085/auth/login 


### Production

```
export APP_SETTINGS="config.ProductionConfig"
```
