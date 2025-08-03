import gradio as gr
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")  # Make sure this file is uploaded to HF Space
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://technews-edbb9-default-rtdb.firebaseio.com/'
    })

# Function to insert subscriber
def subscribe(name, email, category):
    if not name.strip() or not email.strip():
        return "Please enter both name and email."

    ref = db.reference("subscribers")
    data = ref.get()

    if data:
        for entry in data.values():
            if entry.get("email") == email:
                return f" {email} is already subscribed."

    new_ref = ref.push()
    new_ref.set({
        "name": name.strip(),
        "email": email.strip(),
        "category": category.strip()
    })
    return f" Subscribed {name} successfully!"

# Tech categories
categories = [
    "Artificial Intelligence",
    "Machine Learning",
    "Linux & Open Source",
    "Cybersecurity",
    "Cloud Computing",
    "Web Development",
    "Blockchain & Crypto",
    "Programming Languages",
    "DevOps",
    "Tech Startups",
    "Research & Academia",
    "Gadgets & Consumer Tech"
]

# Gradio UI
with gr.Blocks() as app:
    gr.Markdown("# Sign Up for Daily Tech News")
    with gr.Row():
        name = gr.Textbox(label="Your Name")
        email = gr.Textbox(label="Your Email")
    category = gr.Dropdown(label="Choose Your Tech Category", choices=categories, value="Artificial Intelligence")
    submit = gr.Button("Subscribe")
    output = gr.Textbox(label="Status")

    submit.click(fn=subscribe, inputs=[name, email, category], outputs=output)

app.launch()

