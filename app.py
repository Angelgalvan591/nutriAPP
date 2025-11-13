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

# Nueva sección de calculadoras nutricionales angangangang
@app.route('/calculadoras')
def calculadoras():
    return render_template('calculadoras.html')

# 💪 IMC
@app.route('/imc', methods=['GET', 'POST'])
def imc():
    resultado = None
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura']) / 100
        imc = peso / (altura ** 2)

        if imc < 18.5:
            estado = "Bajo peso"
        elif imc < 25:
            estado = "Normal"
        elif imc < 30:
            estado = "Sobrepeso"
        else:
            estado = "Obesidad"

        resultado = f"Tu IMC es {imc:.2f} ({estado})"
    return render_template('imc.html', resultado=resultado)

# 🔥 TMB
@app.route('/tmb', methods=['GET', 'POST'])
def tmb():
    resultado = None
    if request.method == 'POST':
        sexo = request.form['sexo']
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        edad = int(request.form['edad'])

        if sexo == "masculino":
            tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
        else:
            tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

        resultado = f"Tu TMB es {tmb:.2f} calorías/día"
    return render_template('tmb.html', resultado=resultado)

# 🏃‍♂ Gasto Calórico Total
@app.route('/gct', methods=['GET', 'POST'])
def gct():
    resultado = None
    if request.method == 'POST':
        tmb = float(request.form['tmb'])
        actividad = float(request.form['actividad'])
        gct = tmb * actividad
        resultado = f"Tu Gasto Calórico Total es {gct:.2f} calorías/día"
    return render_template('gct.html', resultado=resultado)

# ⚖ Peso Ideal
@app.route('/pesoideal', methods=['GET', 'POST'])
def pesoideal():
    resultado = None
    if request.method == 'POST':
        altura = float(request.form['altura']) / 100
        genero = request.form['genero']
        if genero == "masculino":
            peso_ideal = 22 * (altura ** 2)
        else:
            peso_ideal = 21 * (altura ** 2)
        resultado = f"Tu peso ideal aproximado es {peso_ideal:.1f} kg"
    return render_template('pesoideal.html', resultado=resultado)

# 🥗 Macronutrientes
@app.route('/macronutrientes', methods=['GET', 'POST'])
def macronutrientes():
    resultado = None
    if request.method == 'POST':
        calorias = float(request.form['calorias'])
        proteinas = (calorias * 0.3) / 4
        grasas = (calorias * 0.25) / 9
        carbohidratos = (calorias * 0.45) / 4
        resultado = f"Proteínas: {proteinas:.1f}g | Grasas: {grasas:.1f}g | Carbohidratos: {carbohidratos:.1f}g"
    return render_template('macronutrientes.html', resultado=resultado)



if __name__ == '__main__':
    app.run(debug=True)
