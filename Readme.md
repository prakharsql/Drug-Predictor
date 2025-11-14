# Drug Predictor (FastAPI + HTML Frontend)

## Overview
Predict drug category using a trained ML model served with FastAPI + Jinja2 HTML frontend.

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
