from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Charan'
@app.route('/version')
def new_route():
    response_data="Hi there!"
    return jsonify(response_data),200
@app.errorhandler(404)
def not_found(error):
    return "Page not Found",404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)
