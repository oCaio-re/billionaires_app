from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/hello')
def hello_world_2():
    return 'Hello World! 2'

if __name__ == '__main__':
    app.run()
