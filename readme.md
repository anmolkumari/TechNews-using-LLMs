# TechNews

**TechNews** is an AI-powered daily tech news summarizer. It retrieves the latest tech news from the past 24 hours, summarizes it using prompt-engineered LLMs, and emails personalized updates to subscribed users based on selected categories. https://huggingface.co/spaces/A1nmol/tech-news-app

## Features

- News scraped using Python-integrated tools.
- Summarization via GPT-based frontier models with prompt tuning.
- User interface built with Gradio for category selection and signup. https://huggingface.co/spaces/A1nmol/tech-news-app
- Realtime user database managed using Firebase.
- Scheduled execution via cron for daily runs.
- Emails formatted using SMTP and MIME with model-generated Markdown for clean rendering.
- Deployed on Hugging Face Spaces.

## Tech Stack

| Component        | Technology                        |
|------------------|-----------------------------------|
| Backend          | Python, OpenAI `chat.completions` |
| Summarization    | GPT-based frontier LLMs           |
| UI               | Gradio                            |
| Hosting          | Hugging Face Spaces               |
| Email Delivery   | SMTP, MIME                        |
| Scheduling       | Cron                              |
| Realtime DB      | Firebase                          |
| News Retrieval   | Tool-based dynamic fetchers       |

<img width="1638" height="512" alt="technews_ui" src="https://github.com/user-attachments/assets/a56384f7-01a3-46fa-82ef-5a6016bd9040" />
