#!/usr/bin/env python
# coding: utf-8

# In[21]:


import openai
import os
from dotenv import load_dotenv
from datetime import datetime
# !pip install markdown
import markdown
import firebase_admin
from firebase_admin import credentials, db
# Load .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# In[22]:


# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")  # path to downloaded key
    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://technews-edbb9-default-rtdb.firebaseio.com/'
})


# In[23]:


import requests

def fetch_top_headlines(api_key, query, page_size=5):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "pageSize": page_size,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": api_key,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch news for {query}")
        return []

    data = response.json()
    return data.get("articles", [])


# In[24]:


def summarize_news_with_gpt(headlines,name,category):

    today = datetime.now().strftime("%A, %B %d, %Y")

    prompt = f"""
        You are a friendly yet professional AI assistant named TechNews. 
        Your job is to send a daily news digest email to the name received in param, summarizing the top news headlines:{headlines} of the day in a warm and elegant format.
        Today's date: {today} . Don't use the subject keyword in the email Your task is to write a warm and concise daily tech news summary for the user named {name}, focusing only on the topic: **{category}**.

        Below are the latest headlines related to {category}. Summarize them in a friendly, digestible format suitable for email.

        Here are the headlines you need to summarize based on the {category}:
    """
    for i, article in enumerate(headlines, 1):
        title = article.get("title", "").strip()
        desc = article.get("description", "").strip() or "No description available."
        prompt += f"{i}. {title} - {desc}\n"

    prompt += "\nSummary:\n"
    

    response = openai.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional news summarizer who finds and shares the latest tech news based on category."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.7
    )

    summary = response.choices[0].message.content
    return summary


# In[25]:


def convert_markdown_to_html(markdown_text):
    html = markdown.markdown(markdown_text)
    return html


# In[26]:

os.environ["EMAIL_ADDRESS"] = "techiesparadise@gmail.com"
os.environ["EMAIL_PASSWORD"] = "pbwo ltcj tiyl igmy"


# In[27]:


def get_all_subscribers():
    ref = db.reference("/subscribers")
    data = ref.get()

    if not data:
        return []

    return [(v['name'], v['email'], v['category']) for v in data.values()]


# In[28]:


def send_email_html(subject, markdown_body, sender, password, recipient):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import markdown

    # Convert Markdown to HTML
    html_body = markdown.markdown(markdown_body)

    # Create MIME message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipient) if isinstance(recipient, list) else recipient


    # Attach plain text and HTML parts
    msg.attach(MIMEText(markdown_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# In[30]:


from collections import defaultdict

news_cache = defaultdict(list)

for name, email, category in get_all_subscribers():
    print(f"Sending to: {name} <{email}> – Topic: {category}")

    if not news_cache[category]:
        news_cache[category] = fetch_top_headlines(NEWS_API_KEY, query=category, page_size=5)

    headlines = news_cache[category]

    if not headlines:
        continue  # Skip if nothing fetched

    summary = summarize_news_with_gpt(headlines, name, category)

    send_email_html(
        subject=f"{name}, here’s your personalized {category} Tech News ",
        markdown_body=summary,
        sender=os.getenv("EMAIL_ADDRESS"),
        password=os.getenv("EMAIL_PASSWORD"),
        recipient=email
    )


# In[ ]:




