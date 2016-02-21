import requests

r = requests.get('http://api.github.com/user', auth = ('user','pass'))
r.status_code

if r.status_code == 200:
	print 'Logged in successful'
else:
	print'Check username and password'