# 🌊 AI Drag-Drop Chatbot Creator – Backend (Orange Waves)

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn" />
</p>

> **The robust REST API powering the visual chatbot maker.** 
> Securely handles conversational logic, user profiles, authentication, and data persistence behind the scenes.

**Orange Waves Backend** is the Python-based engine designed to support the drag-and-drop frontend application. Built entirely on the Django framework, it provides seamless data handling, gamified profile metrics, dynamic test series, and integrated blogging capabilities.

---

## 🚀 Core Features

* **Smartbot Core & Auth:** Handles the central application routing, secure token generation, and social login integrations (`smartbot/socialLogin.py`, `smartbot/tokens.py`).
* **Advanced User Profiles:** Manages user data including momentum points, tests attempted, test series, and practical simulations (`profiles/models.py`, `profiles/views.py`).
* **Integrated Blog System:** Fully featured blogging engine with background handling, posts, and serializers (`blog/models.py`, `blog/serializers.py`).
* **Media & Cloud Storage Management:** Organized static asset handling and media uploads (`static_cdn/media_root`), alongside cloud storage configurations (`r2.txt`).
* **Production-Ready Server:** Pre-configured with WSGI/ASGI and Gunicorn for seamless, scalable deployments (`wsgi.py`, `asgi.py`, `Procfile`).

---

## 💻 Tech Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Framework** | ![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white) (`manage.py`, `smartbot/settings.py`) |
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) (`requirements.txt`) |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat-square&logo=sqlite&logoColor=white) (`db.sqlite3` / `mydatabase`) |
| **Server** | ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat-square&logo=gunicorn&logoColor=white) (`Procfile`) |

---

## 📂 Project Structure Overview

The repository is organized into modular Django apps to separate concerns and maintain clean business logic:

* **`/smartbot`**: The core project directory containing global settings, URL routing, social login logic, and WSGI/ASGI configurations.
* **`/profiles`**: App responsible for user interactions, tracking momentum points, managing test questions (with video solutions), and topics.
* **`/blog`**: App dedicated to content management, housing blog post models, migrations, and API views.
* **`/static_cdn`**: Directory for serving static files, chatbot audio assets (`newdin.wav`, `startding.wav`), and uploaded media bundles.
* **`manage.py`**: Django's command-line utility for executing administrative tasks like migrations and running the dev server.
* **`requirements.txt`**: The definitive list of Python dependencies required to run the environment.

---

## ⚙️ Local Development Setup

### 1. Create a Virtual Environment
Ensure you have Python installed, then create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
