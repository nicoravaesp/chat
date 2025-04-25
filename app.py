from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Cargar variables de entorno desde .env
load_dotenv()

# Inicializar cliente OpenAI con clave desde variable de entorno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

mensajes = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    mensajes.append({"role": "user", "content": user_input})

    # Añadir instrucción de formato HTML si no existe
    if not any(m["role"] == "system" for m in mensajes):
        mensajes.insert(0, {
            "role": "system",
            "content": (
                "Responde siempre en HTML básico. Usa etiquetas como <strong>, <ul>, <li>, <a>, <em>, <br> "
                "para enriquecer las respuestas si es útil para el usuario. No expliques las etiquetas."
            )
        })

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=mensajes,
        temperature=0.2,
        max_tokens=400
    )

    respuesta = completion.choices[0].message.content.strip()
    mensajes.append({"role": "assistant", "content": respuesta})

    # Guardar en historial.txt en formato enriquecido
    with open("historial.txt", "a", encoding="utf-8") as f:
        f.write(f"<p><strong>Usuario:</strong> {user_input}</p>\n")
        f.write(f"<p><strong>Bot:</strong> {respuesta}</p>\n<hr>\n")

    return jsonify({"response": respuesta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

