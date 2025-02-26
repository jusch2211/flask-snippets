from flask import Flask, jsonify

app = Flask(__name__)

# Gibt Antworten direkt als String zurück, offentsichtlich nicht die skaliebarste Lösung...
@app.route('/', methods=['GET'])
def get_index():
    return "Wer dies liest ist doof"


@app.route('/testmitformat', methods=['GET'])
def get_testmitformat():
    return "<html><head><title>Test und so</title></head><h1>Wer dies liest ist doof</h1></html>"

if __name__ == '__main__':
    app.run(debug=True)
