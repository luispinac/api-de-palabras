from flask import Flask, request, jsonify
import csv
import random
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "palabras.csv")

# Leer CSV al iniciar la app
palabras = []
with open(CSV_PATH, "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        palabras.append({
            "palabra": fila["palabra"],
            "categoria": fila["categoria"]
        })


@app.route("/") 
def home():
    return "API de palabras en Flask - Funciona correctamente 😉"

# /palabras?cantidad=5
@app.route("/palabras")
def palabras_aleatorias(): 
    cantidad = int(request.args.get("cantidad", 2))
    seleccionadas = random.sample(palabras, min(cantidad, len(palabras)))
    return jsonify(seleccionadas)

@app.route("/categorias")
def listar_categorias():
    categorias = []
    for p in palabras:
        cat = p["categoria"].lower()
        if cat not in categorias:
            categorias.append(cat)
    return jsonify(sorted(categorias))

# /palabras/categoria?tipo=animales
@app.route("/palabras/categoria")
def palabras_por_categoria():
    categoria = request.args.get("tipo", "").lower()
    filtradas = [p["palabra"] for p in palabras if p["categoria"].lower() == categoria]
    if filtradas:
        return jsonify({"categoria": categoria, "palabras": filtradas})
    return jsonify({"error": "Categoría no encontrada"}), 404

# /palabra/longitud?largo=6
@app.route("/palabra/longitud")
def palabra_por_largo():
    largo = int(request.args.get("largo", 5))
    filtradas = [p["palabra"] for p in palabras if len(p["palabra"]) == largo]
    if filtradas:
        return jsonify({"palabra": random.choice(filtradas)})
    return jsonify({"mensaje": "No hay palabras con esa longitud"}), 404

# /palabra/inicia?letra=p
@app.route("/palabra/inicia")
def palabra_por_letra():
    letra = request.args.get("letra", "a").lower()
    filtradas = [p["palabra"] for p in palabras if p["palabra"].startswith(letra)]
    if filtradas:
        return jsonify({"palabra": random.choice(filtradas)})
    return jsonify({"mensaje": "No hay palabras con esa letra"}), 404

if __name__ == "__main__":
    app.run(debug=True)
