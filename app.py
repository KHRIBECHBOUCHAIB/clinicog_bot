import nltk
from nltk.tokenize import word_tokenize
import streamlit as st
import hmac
import hashlib



nltk.data.path.append("C:\\Users\\khrib\\OneDrive\\Bureau\\clinicog_bot\\env\\lib\\nltk_data")  # Update this path
# Download the required NLTK data packages
nltk_data_packages = ["punkt", "averaged_perceptron_tagger", "stopwords"]
for package in nltk_data_packages:
    nltk.download(package)

def check_password():
    """Prompt the user for a password and check if it's correct."""
    if 'password_correct' not in st.session_state or not st.session_state['password_correct']:
        with st.form(key='Password_form'):
            password_input = st.text_input("Enter your password:", type="password", placeholder="Type your password here")
            submit_button = st.form_submit_button("Submit")

            if submit_button and password_input:
                # Hash the input using the secret key from secrets.toml
                hashed_input = hmac.new(
                    key=st.secrets["secret_key"].encode(),
                    msg=password_input.encode(),
                    digestmod=hashlib.sha256
                ).hexdigest()

                # Compare the hash of the input password with the stored hash
                if hmac.compare_digest(hashed_input, st.secrets["password_hash"]):
                    st.session_state["password_correct"] = True
                else:
                    st.session_state["password_correct"] = False
                    st.error("Password incorrect. Please try again.")

    return st.session_state.get("password_correct", False)

if not check_password():
    st.stop()  # Stop execution of the app if the password is incorrect
else:

# Function to load and apply CSS
 def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply the CSS
 local_css("style.css")  # or "styles/style.css" if you put it in a styles directory

# Load your logo image
logo = "images/logo.jpg"
st.image(logo, width=100)

# Extended list of known phrases to include greetings, general inquiries, and psychology content in both English and French
phrases = ["adhd", "tdah", "add", "anxiety", "depression", "hello", "hi", "salut", "bonjour", 
           "how are you", "comment vas-tu", "comment ça va", "how can I help with psychology", 
           "comment puis-je aider avec la psychologie", "what is your symptom", "quels sont vos symptômes", "clinicog", "clinique"]

# Title and logo
st.image(logo, use_column_width=True)
st.title("ClinicoGPT - Votre assistant de santé mentale")

# User input
user_input = st.text_input("Posez votre question ou décrivez vos symptômes:", "")

def respond_to_input(input_text):
    tokens = word_tokenize(input_text.lower())
    responses = {
        "adhd_tdah": "Le TDAH (ADHD en anglais) est un trouble neurodéveloppemental caractérisé par de l'inattention, de l'hyperactivité et de l'impulsivité. Il affecte les enfants et les adultes et peut être géré avec des médicaments, des thérapies et des ajustements de mode de vie.",
        "add": "Le TDA est semblable au TDAH mais se concentre sur l'inattention sans hyperactivité. Il est géré avec des médicaments, des thérapies comportementales et des changements de mode de vie.",
        "anxiety": "L'anxiété implique une inquiétude et une peur affectant la vie quotidienne. Elle est traitable avec des médicaments, des thérapies et des changements de mode de vie.",
        "depression": "La dépression se caractérise par une tristesse persistante et un manque d'intérêt pour les activités. Elle est traitable avec des médicaments et des thérapies.",
        "greeting": "Bonjour ! Je suis là pour vous aider avec toutes vos questions sur la santé mentale. Comment puis-je vous assister aujourd'hui ?",
        "how_are_you": "Je suis un bot, donc je n'ai pas de sentiments, mais je suis là pour vous aider ! Avez-vous des questions sur la santé mentale ?",
        "clinicog": "CLINICOG est une clinique spécialisée dans la santé mentale située à Nancy. Depuis notre création en 2019, nous nous concentrons sur l'expertise de projets innovants et la conception d'outils open source pour les professionnels de la santé. En plus de développer ces ressources, nous accueillons des patients dans le cadre de recherches translationnelles pour faire le pont entre la science et la pratique clinique."
    }
    
    if any(phrase in input_text.lower() for phrase in phrases):
        if "adhd" in tokens or "tdah" in tokens:
            return responses["adhd_tdah"]
        elif "add" in tokens:
            return responses["add"]
        elif "anxiety" in tokens:
            return responses["anxiety"]
        elif "depression" in tokens:
            return responses["depression"]
        elif any(phrase in tokens for phrase in ["hello", "hi", "salut", "bonjour"]):
            return responses["greeting"]
        elif any(phrase in input_text.lower() for phrase in ["how are you", "comment vas-tu", "comment ça va"]):
            return responses["how_are_you"]
        elif "clinicog" in tokens or "clinique" in tokens:
            return responses["clinicog"]
    else:
        return "Je n'ai pas compris votre saisie. Pourriez-vous utiliser des mots-clés comme TDAH, anxiété, dépression, ou me poser des questions sur CLINICOG ?"

if st.button("Envoyer") and user_input:
    response = respond_to_input(user_input)
    st.write(response)
