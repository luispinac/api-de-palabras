from flask import Flask, request, jsonify
import random

import os
import psycopg2

def conectar():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

app = Flask(__name__)
# DB_PATH = "palabras.db"

@app.route("/") 
def home():
    return "API de palabras en Flask - Funciona correctamente 😉"

@app.route("/palabras")
def palabras_aleatorias():
    cantidad = int(request.args.get("cantidad", 1))
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT palabra, categoria FROM palabras")
    todas = cursor.fetchall()
    conn.close()

    seleccionadas = random.sample(todas, min(cantidad, len(todas)))
    return jsonify([{"palabra": p[0], "categoria": p[1]} for p in seleccionadas])

@app.route("/palabras/categoria")
def palabras_por_categoria():
    categoria = request.args.get("tipo", "").lower()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT palabra FROM palabras WHERE LOWER(categoria) = ?", (categoria,))
    resultado = [fila[0] for fila in cursor.fetchall()]
    conn.close()

    if resultado:
        return jsonify({"categoria": categoria, "palabras": resultado})
    return jsonify({"error": "Categoría no encontrada"}), 404

@app.route("/palabra/longitud")
def palabra_por_largo():
    largo = int(request.args.get("largo", 5))
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT palabra FROM palabras WHERE LENGTH(palabra) = ?", (largo,))
    resultado = [fila[0] for fila in cursor.fetchall()]
    conn.close()

    if resultado:
        return jsonify({"palabra": random.choice(resultado)})
    return jsonify({"mensaje": "No hay palabras con esa longitud"}), 404

@app.route("/palabra/inicia")
def palabra_por_letra():
    letra = request.args.get("letra", "a").lower()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT palabra FROM palabras WHERE LOWER(palabra) LIKE ?", (letra + "%",))
    resultado = [fila[0] for fila in cursor.fetchall()]
    conn.close()

    if resultado:
        return jsonify({"palabra": random.choice(resultado)})
    return jsonify({"mensaje": "No hay palabras con esa letra"}), 404

@app.route("/categorias")
def listar_categorias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM palabras")
    categorias = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    return jsonify(categorias)

if __name__ == "__main__":
    app.run(debug=True)
