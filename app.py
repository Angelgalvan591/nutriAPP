from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recetas')
def recetas():
    return render_template('recetas.html')

@app.route('/contadorcal')
def contadorcal():
    return render_template('contadorcal.html')

@app.route('/iniciosesion')
def iniciosesion():
    return render_template('iniciosesion.html')

@app.route('/crearcuenta')
def crearcuenta():
    return render_template('crearcuenta.html')


if __name__ == '__main__':
    app.run(debug=True)