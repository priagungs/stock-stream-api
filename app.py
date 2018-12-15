from flask import Flask, jsonify, request
from flask import stream_with_context, request, Response
import json
import random
import datetime

app = Flask(__name__)
with open('data.json') as file:
    raw = file.read()
    data = json.loads(raw)

def generate_response(size):
    raw = random.choices(data, k=size)
    response = []
    start_time = datetime.datetime.now()
    for el in raw:
        el["timestamp"] = start_time + datetime.timedelta(minutes=random.randrange(60))
        el["high"] = random.randrange(1, 2000)
        el["low"] = random.randrange(0, el["high"])
        el["avg"] = round(random.uniform(el["low"], el["high"]), 2)
        el["last"] = random.randrange(el["low"], el["high"])
        el["value"] = round(random.uniform(10000, 1000000), 2)
        response.append(el)
    return sorted(response, key=lambda element: element['timestamp'], reverse=True)

# usage: localhost/4992/getstream?size='number'
@app.route('/getstream', methods=['GET'])
def stream_response():
    return jsonify(generate_response(int(request.args.get('size'))))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4992, debug=True)
