from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from utils import clean_text

app = Flask(__name__)

# Charger le modèle et le tokenizer
model = load_model("model/model.h5")
with open("model/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

max_len = 100

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if "email" not in data:
        return jsonify({"error": "Aucun email fourni"}), 400

    text = clean_text(data["email"])
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=max_len, padding='post')
    prediction = model.predict(padded)[0][0]
    result = "SPAM" if prediction > 0.5 else "NON SPAM"

    return jsonify({"prediction": result, "score": float(prediction)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

