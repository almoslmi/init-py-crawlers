from flask import Flask, render_template, flash, request
app = Flask(__name__)
app.secret_key = 'guess'

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():
	return render_template('tree.html')


@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():
	return render_template('tree.html')

if __name__ == '__main__':
	app.run(debug = True)