import streamlit as st
import requests

st.title("Détecteur de Spam")

email_input = st.text_area("Entrez le contenu de l'email ici:")

if st.button("Analyser"):
    if email_input.strip() == "":
        st.warning("Veuillez entrer un texte.")
    else:
        response = requests.post("https://api-flask-dl.onrender.com/predict", json={"email": email_input})
        if response.status_code == 200:
            result = response.json()
            st.write("### Résultat :")
            st.success(f"{result['prediction']} (score : {result['score']:.2f})")
        else:
            st.error("Erreur dans la requête à l'API.")
