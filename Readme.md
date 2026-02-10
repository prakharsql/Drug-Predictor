# 💊 Drug Category Predictor

A full-stack Machine Learning web application that predicts the **drug category**
based on input features using a trained ML model, served via **FastAPI** with an
**HTML (Jinja2) frontend**.

---

## 📌 Overview
This project demonstrates how to deploy a trained machine learning model using
FastAPI and serve predictions through a simple web interface.

The application:
- Takes user input from an HTML form
- Sends data to a FastAPI backend
- Uses a trained SVM model to predict the drug category
- Displays the result on a web page

## Structure
- `backend/app` — FastAPI application code (routes, model, config)
- `frontend/templates` — Jinja2 templates (index & result)
- `frontend/static` — CSS styles
- `backend/hyper_para_svm.joblib` — trained model file 

## Local run (dev)
1. Install dependencies:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
