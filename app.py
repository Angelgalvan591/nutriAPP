from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
import re
from functools import wraps

app = Flask(__name__)

#  CONFIG DE LA API Y BASE DE DATOS

app.config['SECRET_KEY'] = 'una_clave_secreta_muy_larga_y_compleja_1234567890'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nutriapp_vogd'

mysql = MySQL(app)

USDA_API_KEY = "ESPULNEPTXufMneVYTlvu1SIXdiOr6Xl1dZJ0AZ5"
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DETAIL_URL = "https://api.nal.usda.gov/fdc/v1/food/"

#  BASE DE DATOS 

def crear_tabla_usuarios():
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
            FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE
        )
    """)

    mysql.connection.commit()
    cursor.close()


def convertir_a_gramos(texto):
    texto = texto.lower().strip()
    numeros = re.findall(r"[\d\.]+", texto)
    cantidad = float(numeros[0]) if numeros else 0

    if "kg" in texto:
        return cantidad * 1000
    if "g" in texto:
        return cantidad
    if "taza" in texto:
        return cantidad * 120
    if "cucharada" in texto:
        return cantidad * 15
    if "cucharadita" in texto:
        return cantidad * 5
    if "pieza" in texto or "unidad" in texto:
        return cantidad * 50

    return cantidad


# ------------------------- USDA CACHE -------------------------

cache_usda = {}


def obtener_info_ingrediente(ingrediente, cantidad_gramos=100):
    # Valores básicos por 100g
    valores_basicos = {
        "manzana": {"cal": 52, "prot": 0.3, "gras": 0.2, "carb": 14},
        "apple": {"cal": 52, "prot": 0.3, "gras": 0.2, "carb": 14},
        "pollo": {"cal": 165, "prot": 31, "gras": 3.6, "carb": 0},
        "chicken": {"cal": 165, "prot": 31, "gras": 3.6, "carb": 0},
        "huevo": {"cal": 155, "prot": 13, "gras": 11, "carb": 1.1},
        "egg": {"cal": 155, "prot": 13, "gras": 11, "carb": 1.1},
        "arroz": {"cal": 130, "prot": 2.7, "gras": 0.3, "carb": 28},
        "rice": {"cal": 130, "prot": 2.7, "gras": 0.3, "carb": 28},
        "pan": {"cal": 265, "prot": 9, "gras": 3.2, "carb": 49},
        "bread": {"cal": 265, "prot": 9, "gras": 3.2, "carb": 49},
        "leche": {"cal": 42, "prot": 3.4, "gras": 1, "carb": 5},
        "milk": {"cal": 42, "prot": 3.4, "gras": 1, "carb": 5}
    }
    
    try:
        search_params = {
            "api_key": USDA_API_KEY,
            "query": ingrediente,
            "pageSize": 1
        }
        search = requests.get(SEARCH_URL, params=search_params, timeout=3)
        
        if search.status_code == 200:
            datos = search.json()
            if "foods" in datos and len(datos["foods"]) > 0:
                fdc_id = datos["foods"][0]["fdcId"]
                detail = requests.get(DETAIL_URL + str(fdc_id), params={"api_key": USDA_API_KEY}, timeout=3)
                
                if detail.status_code == 200:
                    info = detail.json()
                    calorias = proteinas = grasas = carbohidratos = 0
                    
                    for n in info.get("foodNutrients", []):
                        nutrient = n.get("nutrient", {})
                        nutrient_id = nutrient.get("id")
                        valor = n.get("amount") or n.get("value") or 0
                        
                        if nutrient_id == 1008:
                            calorias = valor
                        elif nutrient_id == 1003:
                            proteinas = valor
                        elif nutrient_id == 1004:
                            grasas = valor
                        elif nutrient_id == 1005:
                            carbohidratos = valor
                    
                    factor = max(cantidad_gramos, 1) / 100
                    return {
                        "fdc_id": fdc_id,
                        "ingrediente": ingrediente,
                        "cantidad_gramos": cantidad_gramos,
                        "calorias": round(calorias * factor, 2),
                        "proteinas": round(proteinas * factor, 2),
                        "grasas": round(grasas * factor, 2),
                        "carbohidratos": round(carbohidratos * factor, 2)
                    }
    except:
        pass
    
    ing_lower = ingrediente.lower().strip()
    valores = valores_basicos.get(ing_lower)
    
    if not valores:
        for key, val in valores_basicos.items():
            if key in ing_lower or ing_lower in key:
                valores = val
                break
    
    if not valores:
        valores = {"cal": 50, "prot": 2, "gras": 1, "carb": 10}
    
    factor = cantidad_gramos / 100
    return {
        "fdc_id": 0,
        "ingrediente": ingrediente,
        "cantidad_gramos": cantidad_gramos,
        "calorias": round(valores["cal"] * factor, 2),
        "proteinas": round(valores["prot"] * factor, 2),
        "grasas": round(valores["gras"] * factor, 2),
        "carbohidratos": round(valores["carb"] * factor, 2)
    }

# autenticación y gestión de usuarios
def login_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario_correo" not in session:
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("iniciosesion"))
        return f(*args, **kwargs)
    return wrapper


def get_usuario_por_correo(correo):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    user = cursor.fetchone()
    cursor.close()
    return user


def get_usuario_por_correo_o_telefono(x):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s OR telefono = %s", (x, x))
    user = cursor.fetchone()
    cursor.close()
    return user


@app.context_processor
def inject_user():
    if "usuario_correo" in session:
        return dict(usuario_sesion=get_usuario_por_correo(session["usuario_correo"]))
    return dict(usuario_sesion=None)

# INIT DB
with app.app_context():
    crear_tabla_usuarios()
    crear_tablas_recetas()

# RUTA PRINCIPOAL
@app.route('/')
def index():
    return render_template('index.html')

# CREAR CUENTA E INICIO DE SESIÓN
@app.route('/crearcuenta', methods=['GET', 'POST'])
def crearcuenta():
    if request.method == 'POST':
        nombre = request.form.get("nombre")
        paterno = request.form.get("paterno")
        materno = request.form.get("materno")
        apellidos = f"{paterno} {materno}".strip()
        correo = request.form.get("correo").lower()
        telefono = request.form.get("telefono")
        pw = request.form.get("contraseña")
        conf = request.form.get("confirmarcontraseña")

        if pw != conf:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template("crearcuenta.html")

        if get_usuario_por_correo_o_telefono(correo):
            flash("Ya existe una cuenta con ese correo o teléfono.", "danger")
            return render_template("crearcuenta.html")

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO usuarios 
            (nombre, apellidos, correo, telefono, contrasena) 
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellidos, correo, telefono, generate_password_hash(pw)))
        mysql.connection.commit()
        cursor.close()

        session['usuario_correo'] = correo

        flash("Cuenta creada correctamente. ¡Bienvenido!", "success")
        return redirect(url_for('perfil'))

    return render_template('crearcuenta.html')


# INICIO DE SESIÓN
@app.route('/iniciosesion', methods=['GET', 'POST'])
def iniciosesion():
    if request.method == 'POST':
        x = request.form.get("nombre")
        pw = request.form.get("contraseña")
        user = get_usuario_por_correo_o_telefono(x)

        if user and check_password_hash(user['contrasena'], pw):
            session['usuario_correo'] = user['correo']
            return redirect(url_for("perfil"))

        flash("Datos incorrectos.", "danger")

    return render_template('iniciosesion.html')

# CERRAR SESIÓN
@app.route('/cerrarsesion')
def cerrarsesion():
    session.pop('usuario_correo', None)
    flash("Sesión cerrada.", "info")
    return redirect(url_for('index'))

# PERFIL DE USUARIO
@app.route('/perfil')
@login_requerido
def perfil():
    user = get_usuario_por_correo(session['usuario_correo'])
    prefs = user.get("preferencias") or ""
    user["preferencias_lista"] = [p for p in prefs.split(";") if p]
    return render_template("perfil.html", usuario=user)

# ACTUALIZAR PREFERENCIAS
@app.route('/actualizar_preferencias', methods=['POST'])
@login_requerido
def actualizar_preferencias():
    correo = session['usuario_correo']
    user = get_usuario_por_correo(correo)
    prefs_raw = user.get("preferencias") or ""
    prefs = {}

    for item in prefs_raw.split(";"):
        if ":" in item:
            k, v = item.split(":", 1)
            prefs[k] = v

    for campo in ["actividad", "objetivo", "alergias", "experiencia"]:
        val = request.form.get(campo)
        if val:
            prefs[campo.capitalize()] = val

    nuevo = ";".join([f"{k}:{v}" for k, v in prefs.items()])

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET preferencias=%s WHERE correo=%s", (nuevo, correo))
    mysql.connection.commit()
    cursor.close()

    flash("Preferencias actualizadas.", "success")
    return redirect(url_for("perfil"))

# AÑADIR PREFERENCIA
@app.route('/añadir_preferencia', methods=['POST'])
@login_requerido
def añadir_preferencia():
    nueva = request.form.get("nueva_preferencia", "").strip()
    if not nueva:
        flash("Preferencia no válida.", "warning")
        return redirect(url_for("perfil"))

    correo = session['usuario_correo']
    user = get_usuario_por_correo(correo)
    prefs = user.get("preferencias") or ""
    lista = [p for p in prefs.split(";") if p]
    lista.append(nueva)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE usuarios SET preferencias=%s WHERE correo=%s",
        (";".join(lista), correo)
    )
    mysql.connection.commit()
    cursor.close()

    flash("Preferencia añadida.", "success")
    return redirect(url_for("perfil"))

# EDITAR DATOS DE USUARIO
@app.route('/editar_usuario', methods=['POST'])
@login_requerido
def editar_usuario():
    correo = session['usuario_correo']
    user = get_usuario_por_correo(correo)

    campos = ["nombre", "apellidos", "telefono", "edad", "genero", "peso", "altura"]
    nuevos = {}

    for c in campos:
        nuevos[c] = request.form.get(c, user.get(c))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE usuarios SET 
        nombre=%s, apellidos=%s, telefono=%s, edad=%s, sexo=%s, peso=%s, altura=%s 
        WHERE correo=%s
    """, (
        nuevos["nombre"], nuevos["apellidos"], nuevos["telefono"],
        nuevos["edad"], nuevos["genero"], nuevos["peso"], nuevos["altura"],
        correo
    ))
    mysql.connection.commit()
    cursor.close()

    flash("Datos actualizados.", "success")
    return redirect(url_for("perfil"))


# RECETAS 
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

    cursor.execute("SELECT * FROM recetas WHERE id=%s", (id,))
    receta = cursor.fetchone()

    cursor.execute("SELECT * FROM ingredientes_receta WHERE receta_id=%s", (id,))
    ingredientes = cursor.fetchall()

    cursor.execute("SELECT * FROM pasos_receta WHERE receta_id=%s ORDER BY numero_paso ASC", (id,))
    pasos = cursor.fetchall()

    total_cal = total_prot = total_gras = total_carb = 0

    for ing in ingredientes:
        gramos = convertir_a_gramos(ing["cantidad"])
        info = obtener_info_ingrediente(ing["ingrediente"], gramos)
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


#  ANALIZADOR DE INGREDIENTES 
@app.route('/analizador', methods=['GET', 'POST'])
@login_requerido
def analizador():
    ingredientes_resultado = []
    totales = {"calorias": 0, "proteinas": 0, "grasas": 0, "carbohidratos": 0}

    if request.method == "POST":
        ingredientes = request.form.getlist("ingrediente[]")
        cantidades = request.form.getlist("cantidad[]")

        for ing, cant in zip(ingredientes, cantidades):
            gramos = convertir_a_gramos(cant)
            info = obtener_info_ingrediente(ing, gramos)

            if info:
                ingredientes_resultado.append(info)
                totales["calorias"] += info["calorias"]
                totales["proteinas"] += info["proteinas"]
                totales["grasas"] += info["grasas"]
                totales["carbohidratos"] += info["carbohidratos"]

        return render_template(
            "analizador.html",
            ingredientes=ingredientes_resultado,
            totales=totales,
            mostrar_resultado=True
        )

    return render_template("analizador.html", mostrar_resultado=False)

# GUARDAR RECETA PERSONALIZADA
@app.route("/guardar_receta_personalizada", methods=["POST"])
@login_requerido
def guardar_receta_personalizada():
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    ingredientes = request.form.getlist("ingrediente[]")
    cantidades = request.form.getlist("cantidad[]")

    calorias = proteinas = grasas = carbohidratos = 0

    for ing, cant in zip(ingredientes, cantidades):
        info = obtener_info_ingrediente(ing, convertir_a_gramos(cant))
        if info:
            calorias += info["calorias"]
            proteinas += info["proteinas"]
            grasas += info["grasas"]
            carbohidratos += info["carbohidratos"]

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO recetas 
        (nombre, categoria, dificultad, descripcion, calorias_totales, proteinas, grasas, carbohidratos)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (nombre, "Personalizada", "Media", descripcion,
          calorias, proteinas, grasas, carbohidratos))
    receta_id = cursor.lastrowid

    for ing, cant in zip(ingredientes, cantidades):
        cursor.execute("""
            INSERT INTO ingredientes_receta (receta_id, ingrediente, cantidad)
            VALUES (%s, %s, %s)
        """, (receta_id, ing, cant))

    mysql.connection.commit()
    cursor.close()

    flash("Receta creada correctamente.", "success")
    return redirect(url_for("recetas"))

# INFORMACIÓN NUTRICIONAL
@app.route('/sabermas')
def sabermas():
    return render_template('sabermas.html')

# CALCULADORAS NUTRICIONALES
@app.route('/calculadoras')
def calculadoras():
    return render_template('calculadoras.html')

# IMC
@app.route('/imc', methods=['GET', 'POST'])
def imc():
    resultado = None
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura']) / 100
        imc_val = peso / (altura ** 2)

        if imc_val < 18.5:
            estado = "Bajo peso"
        elif imc_val < 25:
            estado = "Normal"
        elif imc_val < 30:
            estado = "Sobrepeso"
        else:
            estado = "Obesidad"

        resultado = f"Tu IMC es {imc_val:.2f} ({estado})"

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
            tmb_val = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
        else:
            tmb_val = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

        resultado = f"Tu TMB es {tmb_val:.2f} calorías/día"

    return render_template('tmb.html', resultado=resultado)

# GCT
@app.route('/gct', methods=['GET', 'POST'])
def gct():
    resultado = None
    if request.method == 'POST':
        tmb = float(request.form['tmb'])
        actividad = float(request.form['actividad'])
        resultado = f"Tu Gasto Calórico Total es {tmb * actividad:.2f} calorías/día"
    return render_template('gct.html', resultado=resultado)

# PESO IDEAL
@app.route('/pesoideal', methods=['GET', 'POST'])
def pesoideal():
    resultado = None
    if request.method == 'POST':
        altura = float(request.form['altura']) / 100
        genero = request.form['genero']

        peso_ideal = (22 if genero == "masculino" else 21) * (altura ** 2)
        resultado = f"Tu peso ideal aproximado es {peso_ideal:.1f} kg"

    return render_template('pesoideal.html', resultado=resultado)

# MACRONUTRIENTES
@app.route('/macronutrientes', methods=['GET', 'POST'])
@login_requerido
def macronutrientes():
    resultado = None
    if request.method == 'POST':
        calorias = float(request.form['calorias'])
        proteinas = (calorias * 0.3) / 4
        grasas = (calorias * 0.25) / 9
        carb = (calorias * 0.45) / 4
        resultado = f"Proteínas: {proteinas:.1f}g | Grasas: {grasas:.1f}g | Carbohidratos: {carb:.1f}g"

    return render_template('macronutrientes.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
