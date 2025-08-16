from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import redis

app = Flask(__name__)
socketio = SocketIO(app)
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

TEMPLATE = '''
<h1>Vote for your favorite!</h1>
<form id="voteForm">
    <button type="submit" name="vote" value="Cats">Cats</button>
    <button type="submit" name="vote" value="Dogs">Dogs</button>
</form>
<h2>Results</h2>
<p id="cats">Cats: 0</p>
<p id="dogs">Dogs: 0</p>

<script src="https://cdn.socket.io/4.4.1/socket.io.min.js"></script>
<script>
    const socket = io();
    const form = document.getElementById('voteForm');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const vote = e.submitter.value;
        fetch('/', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: 'vote=' + vote
        });
    });

    socket.on('update', data => {
        document.getElementById('cats').innerText = 'Cats: ' + data.cats;
        document.getElementById('dogs').innerText = 'Dogs: ' + data.dogs;
    });
</script>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        vote = request.form['vote']
        redis_client.incr(vote)
        broadcast_votes()
        return '', 204
    return render_template_string(TEMPLATE)

def broadcast_votes():
    cats = int(redis_client.get('Cats') or 0)
    dogs = int(redis_client.get('Dogs') or 0)
    socketio.emit('update', {'cats': cats, 'dogs': dogs})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

