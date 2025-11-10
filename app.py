from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

app.config['SECRET_KEY']='una_clave_secreta_muy_larga_y_compleja_1234567890'

usuarios_db = {}

# Datos globales
alimentos_caloricos = [
    {'nombre': 'Manzana', 'calorias': 52},
    {'nombre': 'Pan integral', 'calorias': 69},
    {'nombre': 'Yogurt natural', 'calorias': 59},
    {'nombre': 'Pollo a la plancha', 'calorias': 165},
    {'nombre': 'Arroz cocido', 'calorias': 130}
]

alimentos_clasificados = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recetas')
def recetas():
    return render_template('recetas.html')

@app.route('/contadorcal', methods=['GET', 'POST'])
def contadorcal():
    if request.method == 'POST':
        nombre = request.form['foodItem']
        calorias = float(request.form['calories'])
        alimentos_caloricos.append({'nombre': nombre, 'calorias': calorias})

    total = sum(a['calorias'] for a in alimentos_caloricos)
    return render_template('contadorcal.html', alimentos=alimentos_caloricos, total_calorias=total)

@app.route('/limpiar_calorias', methods=['POST'])
def limpiar_calorias():
    alimentos_caloricos.clear()
    return redirect(url_for('contadorcal'))

@app.route('/clasificador', methods=['GET', 'POST'])
def clasificador():
    if request.method == 'POST':
        nombre = request.form['nombre']
        grasas = float(request.form['grasas'])
        proteinas = float(request.form['proteinas'])
        carbohidratos = float(request.form['carbohidratos'])

        if grasas > proteinas and grasas > carbohidratos:
            clasificacion = 'Alto en grasas'
        elif proteinas > grasas and proteinas > carbohidratos:
            clasificacion = 'Alto en proteínas'
        elif carbohidratos > grasas and carbohidratos > proteinas:
            clasificacion = 'Alto en carbohidratos'
        else:
            clasificacion = 'Balanceado'

        alimentos_clasificados.append({'nombre': nombre, 'clasificacion': clasificacion})

    return render_template('clasificador.html', alimentos_clasificados=alimentos_clasificados)

@app.route('/limpiar_lista', methods=['POST'])
def limpiar_lista():
    alimentos_clasificados.clear()
    return redirect(url_for('clasificador'))

@app.route('/iniciosesion', methods=['GET', 'POST'])
def iniciosesion():
    if request.method == 'POST':
        correo = request.form.get('nombre') 
        contrasena = request.form.get('contraseña')

        if correo in usuarios_db and usuarios_db[correo]['contrasena'] == contrasena:
            session['usuario'] = usuarios_db[correo]
            flash(f'Bienvenido de nuevo, {usuarios_db[correo]["nombre"]}!', 'success')
            return redirect(url_for('perfil'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')

    return render_template('iniciosesion.html')

@app.route('/crearcuenta', methods=['GET', 'POST'])
def crearcuenta():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        correo = request.form.get('correo')
        contrasena = request.form.get('contraseña')
        edad = request.form.get('edad')
        sexo = request.form.get('sexo')
        peso = request.form.get('peso')
        altura = request.form.get('altura')
        actividad = request.form.get('actividad')
        objetivo = request.form.get('objetivo')
        preferencias = request.form.get('preferencias')
        experiencia = request.form.get('experiencia')

        if not nombre or not correo or not contrasena:
            flash("Por favor, completa los campos obligatorios.", "warning")
            return render_template('crearcuenta.html')

        if correo in usuarios_db:
            flash("Ya existe una cuenta con ese correo.", "danger")
            return render_template('crearcuenta.html')

        usuarios_db[correo] = {
            'nombre': nombre,
            'apellidos': apellidos,
            'correo': correo,
            'contrasena': contrasena,
            'edad': edad,
            'sexo': sexo,
            'peso': peso,
            'altura': altura,
            'actividad': actividad,
            'objetivo': objetivo,
            'preferencias': preferencias,
            'experiencia': experiencia
        }

        session['usuario'] = usuarios_db[correo]

        flash(f'Cuenta creada exitosamente. ¡Bienvenido, {nombre}!', 'success')
        return redirect(url_for('perfil'))

    return render_template('crearcuenta.html')

@app.route('/gastoenergetico', methods=['GET', 'POST'])
def gastoenergetico():
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        edad = int(request.form['edad'])
        genero = request.form['genero']
        actividad = float(request.form['actividad'])

        if genero == 'hombre':
            tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
        else:
            tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

        resultado = round(tmb * actividad, 2)
        tmb = round(tmb, 2)

        return render_template('gastoenergetico.html', tmb=tmb, resultado=resultado)

    return render_template('gastoenergetico.html')

@app.route('/perfil')
def perfil():
    usuario = session.get('usuario')
    if not usuario:
        flash('Debes iniciar sesión para ver tu perfil.', 'warning')
        return redirect(url_for('iniciosesion'))
    return render_template('perfil.html', usuario=usuario)

@app.route('/cerrarsesion')
def cerrarsesion():
    session.pop('usuario', None)
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))

@app.route('/sabermas')
def sabermas():
    return render_template('sabermas.html')


if __name__ == '__main__':
    app.run(debug=True)
