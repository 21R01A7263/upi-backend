from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas

app = FastAPI()

# 1. Mount Static Files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Configure HTML Templates
templates = Jinja2Templates(directory="templates")

# --- Web UI Routes (Frontend) ---

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # This serves the Landing Page
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/merchant", response_class=HTMLResponse)
def merchant_ui(request: Request):
    return templates.TemplateResponse("merchant.html", {"request": request})

@app.get("/user", response_class=HTMLResponse)
def user_ui(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})
# --- User Endpoints ---

@app.get("/user/{username}", response_model=schemas.UserResponse)
def get_user_home(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/pay")
def make_payment(payment: schemas.PaymentRequest, db: Session = Depends(get_db)):
    # 1. Identify the Payer (Hardcoded to 'user' for this demo)
    payer = crud.get_user_by_username(db, "user")
    if not payer:
        raise HTTPException(status_code=404, detail="Payer account not found. Did you run seed.py?")
    
    # 2. Process the Payment
    result = crud.process_payment(db, payment=payment, sender_id=payer.id)
    
    # 3. Handle Errors
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

# --- Merchant Endpoints ---

@app.get("/merchant/{handle}")
def get_merchant_dashboard(handle: str, db: Session = Depends(get_db)):
    # 1. Get Merchant Details
    merchant = crud.get_merchant_by_handle(db, handle)
    if merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    # 2. Get Transaction History
    history = crud.get_merchant_history(db, merchant.id)
    
    # 3. Construct Response
    return {
        "merchant": merchant,
        "history": history
    }