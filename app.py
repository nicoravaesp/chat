from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Inicializar la app Flask
app = Flask(__name__)

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Inicializar el cliente de OpenAI con clave desde variable de entorno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Lista para mantener el historial del chat
mensajes = []

# Ruta principal que carga la interfaz del chatbot
@app.route("/")
def index():
    return render_template("index.html")

# Ruta del endpoint para el chat
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    mensajes.append({"role": "user", "content": user_input})

    # Instrucción para respuestas en HTML enriquecido (solo una vez)
    if not any(m["role"] == "system" for m in mensajes):
        mensajes.insert(0, {
            "role": "system",
            "content": (
                "Responde siempre en HTML básico. Usa etiquetas como <strong>, <ul>, <li>, <a>, <em>, <br> "
                "para enriquecer las respuestas si es útil para el usuario. No expliques las etiquetas."
            )
        })

    # Generar respuesta con OpenAI
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=mensajes,
        temperature=0.2,
        max_tokens=400
    )

    respuesta = completion.choices[0].message.content.strip()
    mensajes.append({"role": "assistant", "content": respuesta})

    # Guardar historial enriquecido en archivo
    with open("historial.txt", "a", encoding="utf-8") as f:
        f.write(f"<p><strong>Usuario:</strong> {user_input}</p>\n")
        f.write(f"<p><strong>Bot:</strong> {respuesta}</p>\n<hr>\n")

    return jsonify({"response": respuesta})

# Ejecutar la aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
