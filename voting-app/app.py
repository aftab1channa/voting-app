from flask import Flask, render_template_string, request
import redis

app = Flask(__name__)
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

TEMPLATE = '''
<h1>Vote for your favorite!</h1>
<form method="POST">
    <button name="vote" value="Cats">Cats</button>
    <button name="vote" value="Dogs">Dogs</button>
</form>
<p>Cats: {{ cats }}</p>
<p>Dogs: {{ dogs }}</p>
'''

@app.route('/', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        vote = request.form['vote']
        redis_client.incr(vote)
    cats = redis_client.get('Cats') or 0
    dogs = redis_client.get('Dogs') or 0
    return render_template_string(TEMPLATE, cats=int(cats), dogs=int(dogs))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
