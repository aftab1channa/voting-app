from flask import Flask, render_template_string
import redis

app = Flask(__name__)
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

TEMPLATE = '''
<h1>Voting Results</h1>
<p>Cats: {{ cats }}</p>
<p>Dogs: {{ dogs }}</p>
'''

@app.route('/')
def results():
    cats = redis_client.get('Cats') or 0
    dogs = redis_client.get('Dogs') or 0
    return render_template_string(TEMPLATE, cats=int(cats), dogs=int(dogs))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
