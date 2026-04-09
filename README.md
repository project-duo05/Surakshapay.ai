<div align="center">

<img src="./assets/logo.png" alt="SurakshaPayAI Logo" width="260"/>

# 🛡️ SurakshaPayAI

### 🚀 Production-Grade AI Fraud Detection Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **Stop fraud before it happens.**  
> Real-time AI-powered fraud detection system for banks, fintechs, and payment systems.

</div>

---

## 🚀 Overview

SurakshaPayAI is a **real-time fraud detection platform** that:
- Analyzes transactions instantly  
- Generates a **risk score (0–100)**  
- Takes smart decisions:
  - ✅ Approve  
  - 🔐 OTP  
  - ⚠️ Review  
  - 🚫 Block  

---

## ✨ Features

### 🔴 Live Decision Engine

```
Risk Score = 0.4 × Anomaly + 0.4 × ML + 0.2 × Rules
```

### 🧠 Hybrid AI Model
- Isolation Forest (Anomaly Detection)
- Logistic Regression (Fraud Prediction)
- Rule-Based Engine

### 📊 Dashboard
- KPI Metrics
- Fraud Trends
- Risk Graphs

### 🔔 Alerts System
- High-risk alerts
- Case tracking
- Audit logs

### 🔐 Authentication
- Login/Register system
- Role-based access

---

## ⚡ Quick Start

### 1️⃣ Clone Repository
```bash
git clone https://github.com/project-duo05/Surakshapay.ai.git
cd Surakshapay.ai
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Environment
```bash
cp .env.example .env
```

### 4️⃣ Run Application
```bash
streamlit run app.py
```

👉 Open in browser:  
http://localhost:8501

---

## 🔐 Default Login

```
Email:    admin@surakshapay.ai
Password: admin
```

⚠️ Change credentials in production.

---

## 🏗️ Architecture

```
Transaction
    ↓
Feature Engineering
    ↓
[ Anomaly Model ]
[ ML Model ]
[ Rule Engine ]
    ↓
Hybrid Risk Score
    ↓
Decision Engine
```

---

## 🛠️ Tech Stack

| Layer       | Technology        |
|------------|------------------|
| Frontend   | Streamlit        |
| Backend    | FastAPI          |
| ML Models  | scikit-learn     |
| Database   | SQLite           |
| Data       | Pandas, NumPy    |

---

## 📡 API Example

```http
POST /predict
```

```json
{
  "transaction_id": "TXN123",
  "amount": 5000,
  "location": "Delhi"
}
```

---

## 🧪 Run Tests

```bash
python -m pytest
```

---


---

<div align="center">

### 💡 Built with ❤️ by SurakshaPayAI Team

</div>
