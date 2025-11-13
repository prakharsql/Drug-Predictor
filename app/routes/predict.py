from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import io

from ..services.prediction_service import predict_single_service, predict_batch_service

templates = Jinja2Templates(directory="app/frontend/templates")

router = APIRouter(prefix="/predict", tags=["Prediction"])

# 👉 ADD THIS PART
@router.get("/", response_class=HTMLResponse)
async def show_predict_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def predict_form(request: Request,
                       age: float = Form(...),
                       sex: str = Form(...),
                       bp: str = Form(...),
                       chol: str = Form(...),
                       na_to_k: float = Form(...)):

    try:
        pred = predict_single_service(age, sex, bp, chol, na_to_k)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return templates.TemplateResponse("result.html", {
        "request": request,
        "age": age,
        "sex": sex,
        "bp": bp,
        "chol": chol,
        "na_to_k": na_to_k,
        "prediction": pred
    })


@router.post("/file")
async def predict_file(file: UploadFile = File(...)):

    data = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file: {e}")

    try:
        out = predict_batch_service(df)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {e}")

    stream = io.StringIO()
    out.to_csv(stream, index=False)
    stream.seek(0)
    return PlainTextResponse(content=stream.getvalue(), media_type="text/csv")
