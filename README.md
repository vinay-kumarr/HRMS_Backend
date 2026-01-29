# 🚀 HRMS Lite - Backend

The robust API server for the **HRMS Lite** application, built with **FastAPI** and **MongoDB**.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

---

## 📋 Table of Contents
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running Locally](#-running-locally)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)

---

## ✨ Features
*   **Employee Management**: Create, read, update, and delete employee records.
*   **Attendance Tracking**: Mark and view daily attendance.
*   **Dashboard Analytics**: Real-time stats on workforce.
*   **Scalable Architecture**: Modular structure ready for production.

---

## 🛠 Prerequisites
*   **Python 3.9** or higher.
*   **MongoDB Atlas** account (or local MongoDB).

---

## 📥 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/vinay-kumarr/HRMS_Backend.git
    cd HRMS_Backend
    ```

2.  **Create a Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration**
    Create a `.env` file in the root directory:
    ```ini
    # .env
    MONGODB_URL=mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
    DB_NAME=hrms_lite
    CORS_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app
    ```

---

## 🏃 Running Locally

Start the development server with hot-reload:

```bash
uvicorn app.main:app --reload --port 8001
```

The API will be available at: `http://localhost:8001`

---

## 📑 API Documentation
FastAPI provides automatic interactive documentation.
*   **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)
*   **ReDoc**: [http://localhost:8001/redoc](http://localhost:8001/redoc)

---

## 🚀 Deployment (Render)
This project is configured for **Render.com**.

1.  Push this code to a GitHub repository.
2.  Create a **New Web Service** on Render.
3.  Connect your repo.
4.  **Build Command**: `pip install -r requirements.txt`
5.  **Start Command**: `gunicorn app.main:app -k uvicorn.workers.UvicornWorker`
6.  Add your `MONGODB_URL` in the Environment Variables settings.
