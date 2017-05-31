from flask import Flask, request, session, send_file
import redis, random, string

app = Flask(__name__)
app.config.update(dict(
	DEBUG=False,
	SECRET_KEY='DFWL0G69HUHdeJN'
))
app.config['POOL'] = redis.ConnectionPool(host='127.0.0.1', port=6379)


@app.route('/')
def index():
    return send_file('page.html')

@app.route('/state', methods=['GET'])
def getState():
	r = redis.Redis(connection_pool=app.config['POOL'])
	if session.get('state') and r.get(session['state']):
		return session['state']
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
	r.set(state, 'none', ex=2*60)
	session['state'] = state
	return state

@app.route('/result', methods=['GET'])
def getResult():
	r = redis.Redis(connection_pool=app.config['POOL'])
	if session.get('state') and r.get(session['state']) == 'success':
		return 'success'
	return 'failed'

@app.route('/success', methods=['GET'])
def sendCode():
	state = request.args.get('state')
	code = request.args.get('code')
	r = redis.Redis(connection_pool=app.config['POOL'])
	if r.get(state):
		r.set(state, 'success')
		return code
	return 'failed'


if __name__ == '__main__':
	app.run()


