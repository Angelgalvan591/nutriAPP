from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
import re

app = Flask(__name__)

USDA_API_KEY = "zHYga31MsqopFACKsNz8AWNXvs0h6tyKxULQ9hKz"
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DETAIL_URL = "https://api.nal.usda.gov/fdc/v1/food/"

def obtener_info_ingrediente(ingrediente, cantidad_gramos=100):
    # Buscar ingrediente
    search_params = {
        "api_key": USDA_API_KEY,
        "query": ingrediente,
        "pageSize": 1
    }

    search = requests.get(SEARCH_URL, params=search_params)

    if search.status_code != 200:
        print("Error en búsqueda USDA:", search.text)
        return None

    datos = search.json()
    if "foods" not in datos or len(datos["foods"]) == 0:
        return None

    fdc_id = datos["foods"][0]["fdcId"]

    # Obtener detalle correcto
    detail_params = {
        "api_key": USDA_API_KEY
    }
    detail = requests.get(DETAIL_URL + str(fdc_id), params=detail_params)

    if detail.status_code != 200:
        print("Error detalles USDA:", detail.text)
        return None

    info = detail.json()

    calorias = proteinas = grasas = carbohidratos = 0

    for n in info.get("foodNutrients", []):
        nombre = n.get("nutrient", {}).get("name", "")
        valor = n.get("amount", 0)

        if "Energy" in nombre:
            calorias = valor
        elif "Protein" in nombre:
            proteinas = valor
        elif "lipid" in nombre.lower():
            grasas = valor
        elif "Carbohydrate" in nombre:
            carbohidratos = valor

    factor = cantidad_gramos / 100

    return {
        "fdc_id": fdc_id,
        "ingrediente": ingrediente,
        "cantidad_gramos": cantidad_gramos,
        "calorias": calorias * factor,
        "proteinas": proteinas * factor,
        "grasas": grasas * factor,
        "carbohidratos": carbohidratos * factor
    }

def convertir_a_gramos(texto):
    """
    Convierte strings como '140 g', '1 taza', '2 piezas'
    en gramos aproximados.
    """
    texto = texto.lower().strip()

    # si contiene un número con unidades 
    numero = re.findall(r"[\d\.]+", texto)
    cantidad = float(numero[0]) if numero else 0

    #  detectar unidades 
    if "g" in texto or "gramo" in texto:
        return cantidad
    
    if "kg" in texto:
        return cantidad * 1000

    # unidades comunes que NO son gramos 
    if "taza" in texto:
        return cantidad * 120  
    
    if "cucharada" in texto:
        return cantidad * 15

    if "cucharadita" in texto:
        return cantidad * 5

    if "pieza" in texto or "unidad" in texto:
        return cantidad * 50      # estimado

    # si no se reconoce → devolver número plano
    return cantidad

app.config['SECRET_KEY']='una_clave_secreta_muy_larga_y_compleja_1234567890'

# Configuración de base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'nutriapp_vogd'
mysql = MySQL(app)

def crear_tablas_recetas():
    cursor = mysql.connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recetas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(200) NOT NULL,
            categoria VARCHAR(100) NOT NULL,
            dificultad VARCHAR(50),
            descripcion TEXT,
            calorias_totales FLOAT,
            proteinas FLOAT,
            grasas FLOAT,
            carbohidratos FLOAT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredientes_receta (
            id INT AUTO_INCREMENT PRIMARY KEY,
            receta_id INT,
            ingrediente VARCHAR(200),
            cantidad VARCHAR(100),
            fdc_id INT,
            FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pasos_receta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receta_id INT NOT NULL,
    numero_paso INT NOT NULL,
    descripcion TEXT NOT NULL,
    FOREIGN KEY (receta_id) REFERENCES recetas(id)
        ON DELETE CASCADE
        )
        """)

    mysql.connection.commit()
    cursor.close()
    
def nutrientes_totales(ingredientes):
    totales = {
        "calorias": 0,
        "proteinas": 0,
        "grasas": 0,
        "carbohidratos": 0
    }

    for ing in ingredientes:
        info = obtener_info_ingrediente(ing)
        if info:
            totales["calorias"] += info["calorias"] or 0
            totales["proteinas"] += info["proteinas"] or 0
            totales["grasas"] += info["grasas"] or 0
            totales["carbohidratos"] += info["carbohidratos"] or 0

    return totales

    
def crear_tabla_usuarios():
    """Crea la tabla usuarios si no existe."""
    cursor = mysql.connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100),
            apellidos VARCHAR(200),
            correo VARCHAR(120) UNIQUE,
            telefono VARCHAR(30),
            contrasena VARCHAR(255),
            edad INT,
            sexo VARCHAR(20),
            peso FLOAT,
            altura FLOAT,
            preferencias TEXT
        )
    ''')
    mysql.connection.commit()
    cursor.close()


def get_usuario_por_correo_o_telefono(identificador):
    """
    Busca usuario por correo o por teléfono.
    Devuelve diccionario con campos o None.
    """
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s OR telefono = %s", (identificador, identificador))
    user = cursor.fetchone()
    cursor.close()
    return user


def get_usuario_por_correo(correo):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    user = cursor.fetchone()
    cursor.close()
    return user


def login_requerido(func):
    """Decorator simple para proteger rutas (sin usar flask-login)."""
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'usuario_correo' not in session:
            flash('Debes iniciar sesión para acceder a esta sección.', 'warning')
            return redirect(url_for('iniciosesion'))
        return func(*args, **kwargs)
    return wrapper

# Crear tabla al iniciar
with app.app_context():
    crear_tabla_usuarios()
    crear_tablas_recetas()


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

# Crear cuenta
@app.route('/crearcuenta', methods=['GET', 'POST'])
def crearcuenta():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        paterno = request.form.get('paterno', '').strip()
        materno = request.form.get('materno', '').strip()
        apellidos = f"{paterno} {materno}".strip()
        correo = request.form.get('correo', '').strip().lower()
        telefono = request.form.get('telefono', '').strip()
        contrasena = request.form.get('contraseña', '')
        confirmar = request.form.get('confirmarcontraseña', '')
        edad = request.form.get('edad') or None
        sexo = request.form.get('sexo') or None
        peso = request.form.get('peso') or None
        altura = request.form.get('altura') or None

        # Validaciones
        if not nombre or not correo or not contrasena:
            flash("Por favor, completa los campos obligatorios.", "warning")
            return render_template('crearcuenta.html')

        if contrasena != confirmar:
            flash("Las contraseñas no coinciden.", "warning")
            return render_template('crearcuenta.html')

        if get_usuario_por_correo_o_telefono(correo) is not None:
            flash("Ya existe una cuenta con ese correo o teléfono.", "danger")
            return render_template('crearcuenta.html')

        # hash de contraseña
        hash_pw = generate_password_hash(contrasena)

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellidos, correo, telefono, contrasena, edad, sexo, peso, altura, preferencias)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            nombre, apellidos, correo, telefono, hash_pw,
            int(edad) if edad else None, sexo,
            float(peso) if peso else None, float(altura) if altura else None,
            ''  # preferencias vacío inicialmente
        ))
        mysql.connection.commit()
        cursor.close()

        flash("Cuenta creada correctamente. Inicia sesión.", "success")
        return redirect(url_for('iniciosesion'))

    return render_template('crearcuenta.html')

# Inicio de sesión
@app.route('/iniciosesion', methods=['GET', 'POST'])
def iniciosesion():
    if request.method == 'POST':
        identificador = request.form.get('nombre', '').strip()
        contrasena = request.form.get('contraseña', '')

        usuario = get_usuario_por_correo_o_telefono(identificador)
        if usuario and check_password_hash(usuario['contrasena'], contrasena):
            session['usuario_correo'] = usuario['correo']
            flash(f'Bienvenido de nuevo, {usuario["nombre"]}!', 'success')
            return redirect(url_for('perfil'))
        else:
            flash('Correo/usuario o contraseña incorrectos.', 'danger')

    return render_template('iniciosesion.html')

# para agregar el usuario en todas las plantillas que necesite
@app.context_processor
def inject_user():
    if 'usuario_correo' in session:
        usuario = get_usuario_por_correo(session['usuario_correo'])
        return dict(usuario_sesion=usuario)
    return dict(usuario_sesion=None)

# Perfil de usuario
@app.route('/perfil')
@login_requerido
def perfil():
    correo = session.get('usuario_correo')
    usuario = get_usuario_por_correo(correo)
    if not usuario:
        flash('Usuario no encontrado. Inicia sesión de nuevo.', 'warning')
        session.pop('usuario_correo', None)
        return redirect(url_for('iniciosesion'))

    prefs_text = usuario.get('preferencias') or ''
    preferencias_lista = [p for p in prefs_text.split(';') if p.strip()]
    usuario['preferencias_lista'] = preferencias_lista

    return render_template('perfil.html', usuario=usuario)

# Actualizar preferencias
@app.route('/actualizar_preferencias', methods=['POST'])
@login_requerido
def actualizar_preferencias():
    correo = session.get('usuario_correo')
    usuario = get_usuario_por_correo(correo)

    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('iniciosesion'))

    prefs_text = usuario.get('preferencias') or ""
    prefs_dict = {}

    for parte in prefs_text.split(";"):
        if ":" in parte:
            key, val = parte.split(":", 1)
            prefs_dict[key] = val

    actividad = request.form.get("actividad", "").strip()
    objetivo = request.form.get("objetivo", "").strip()
    alergias = request.form.get("alergias", "").strip()
    experiencia = request.form.get("experiencia", "").strip()

    if actividad:
        prefs_dict["Actividad"] = actividad
    if objetivo:
        prefs_dict["Objetivo"] = objetivo
    if experiencia:
        prefs_dict["Experiencia"] = experiencia
    if alergias:
        prefs_dict["Alergias"] = alergias

    nuevo_texto = ";".join([f"{k}:{v}" for k, v in prefs_dict.items()])

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET preferencias = %s WHERE correo = %s",
                   (nuevo_texto, correo))
    mysql.connection.commit()
    cursor.close()

    flash("Preferencias actualizadas con éxito", "success")
    return redirect(url_for("perfil"))

# Añadir preferencia
@app.route('/añadir_preferencia', methods=['POST'])
@login_requerido
def anadir_preferencia():
    correo = session.get('usuario_correo')
    nueva = request.form.get('nueva_preferencia', '').strip()
    if not nueva:
        flash('Ingresa una preferencia válida.', 'warning')
        return redirect(url_for('perfil'))

    usuario = get_usuario_por_correo(correo)
    prefs_text = usuario.get('preferencias') or ''
    prefs_lista = [p for p in prefs_text.split(';') if p.strip()]
    prefs_lista.append(nueva)
    nueva_text = ';'.join(prefs_lista)

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET preferencias = %s WHERE correo = %s", (nueva_text, correo))
    mysql.connection.commit()
    cursor.close()

    flash('Preferencia añadida.', 'success')
    return redirect(url_for('perfil'))

# Editar datos de usuario
@app.route('/editar_usuario', methods=['POST'])
@login_requerido
def editar_usuario():
    correo = session.get('usuario_correo')
    usuario = get_usuario_por_correo(correo)
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('iniciosesion'))

    nombre = request.form.get('nombre', usuario['nombre']).strip()
    apellidos = request.form.get('apellidos', usuario.get('apellidos', '')).strip()
    telefono = request.form.get('telefono', usuario.get('telefono', '')).strip()
    edad = request.form.get('edad') or None
    sexo = request.form.get('genero', usuario.get('sexo'))
    peso = request.form.get('peso') or None
    altura = request.form.get('altura') or None

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET nombre=%s, apellidos=%s, telefono=%s, edad=%s, sexo=%s, peso=%s, altura=%s
        WHERE correo=%s
    """, (
        nombre, apellidos, telefono,
        int(edad) if edad else None,
        sexo,
        float(peso) if peso else None,
        float(altura) if altura else None,
        correo
    ))
    mysql.connection.commit()
    cursor.close()

    flash('Datos de usuario actualizados.', 'success')
    return redirect(url_for('perfil'))

# Cerrar sesión
@app.route('/cerrarsesion')
def cerrarsesion():
    session.pop('usuario_correo', None)
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))

# recetas
@app.route('/recetas')
def recetas():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM recetas")
    recetas = cursor.fetchall()
    cursor.close()

    return render_template('recetas.html', recetas=recetas)

@app.route('/receta/<int:id>')
def receta_detalle(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM recetas WHERE id = %s", (id,))
    receta = cursor.fetchone()

    cursor.execute("SELECT * FROM ingredientes_receta WHERE receta_id = %s", (id,))
    ingredientes = cursor.fetchall()
    
    cursor.execute("SELECT * FROM pasos_receta WHERE receta_id = %s ORDER BY numero_paso ASC", (id,))
    pasos = cursor.fetchall()

    total_cal = total_prot = total_gras = total_carb = 0

    for ing in ingredientes:
        nombre = ing["ingrediente"]
        
        # convertir texto → gramos
        cantidad_gramos = convertir_a_gramos(ing["cantidad"])

        info = obtener_info_ingrediente(nombre, cantidad_gramos)

        if info:
            total_cal += info["calorias"]
            total_prot += info["proteinas"]
            total_gras += info["grasas"]
            total_carb += info["carbohidratos"]

    receta["calorias_totales"] = round(total_cal, 2)
    receta["proteinas"] = round(total_prot, 2)
    receta["grasas"] = round(total_gras, 2)
    receta["carbohidratos"] = round(total_carb, 2)

    return render_template(
        "receta_detalle.html",
        receta=receta,
        ingredientes=ingredientes,
        pasos=pasos
    )



# Clasificador de alimentos
@app.route('/clasificador', methods=['GET', 'POST'])
@login_requerido
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

# Sección informativa
@app.route('/sabermas')
def sabermas():
    return render_template('sabermas.html')

# Sección de calculadoras nutricionales
@app.route('/calculadoras')
@login_requerido
def calculadoras():
    return render_template('calculadoras.html')

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


#  IMC
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

# TMB
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

#  Gasto Calórico Total
@app.route('/gct', methods=['GET', 'POST'])
def gct():
    resultado = None
    if request.method == 'POST':
        tmb = float(request.form['tmb'])
        actividad = float(request.form['actividad'])
        gct = tmb * actividad
        resultado = f"Tu Gasto Calórico Total es {gct:.2f} calorías/día"
    return render_template('gct.html', resultado=resultado)

# Peso Ideal
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

# Macronutrientes
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

@app.route('/analizador', methods=['GET', 'POST'])
def analizador():
    resultado = None
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form['ingredientes'].lower().split(',')

        # Simulación básica
        calorias = 0
        proteinas = 0
        grasas = 0
        carbohidratos = 0

        for item in ingredientes:
            item = item.strip()
            if "pollo" in item:
                calorias += 165
                proteinas += 31
            elif "queso" in item:
                calorias += 100
                grasas += 8
            elif "tortilla" in item:
                calorias += 70
                carbohidratos += 15
            
        resultado = f"""
        <strong>{nombre.title()}</strong><br>
        Calorías estimadas: {calorias} kcal<br>
        Proteínas: {proteinas}g<br>
        Grasas: {grasas}g<br>
        Carbohidratos: {carbohidratos}g
        """

    return render_template('analizador.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)