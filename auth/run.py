from app import app
from config import HOST
from config import PORT
from config import DEBUG

app.run(host=HOST, port=PORT, debug=DEBUG)
