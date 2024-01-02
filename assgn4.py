from flask import Flask, redirect, request

app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello, Charan'
@app.route('/redirect')
def perform_redirect():
    # Get the value of the "redirect" parameter from the query string
    redirect_value = request.args.get('redirect')

    # Determine the status code based on the parameter value
    if redirect_value == '302':
        return redirect('https://aqfer.com/', code=302)
    elif redirect_value == '301':
        return redirect('https://aqfer.com/', code=301)
    else:
        return 'Invalid redirect value'

if __name__ == '__main__':
    app.run(debug=True)
