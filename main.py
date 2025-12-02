from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
print("Running on http://localhost:8000/")

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