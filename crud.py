from sqlalchemy.orm import Session
from models import User, Merchant, Transaction
from schemas import PaymentRequest
import datetime

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, full_name: str, pin: str, balance: float):
    # Helper to create dummy data easily
    db_user = User(username=username, full_name=full_name, pin=pin, balance=balance)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_merchant(db: Session, handle: str, full_name: str, balance: float):
    # Helper to create dummy merchant
    db_merchant = Merchant(handle=handle, full_name=full_name, balance=balance)
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant

def process_payment(db: Session, payment: PaymentRequest, sender_id: int):
    # 1. Get Sender
    sender = db.query(User).filter(User.id == sender_id).first()
    if not sender:
        return {"error": "Sender not found"}

    # 2. Get Receiver
    receiver = db.query(Merchant).filter(Merchant.handle == payment.receiver_handle).first()
    if not receiver:
        return {"error": "Merchant not found"}

    # 3. Verify PIN
    if sender.pin != payment.pin:
        return {"error": "Invalid PIN"}

    # 4. Check Balance
    if sender.balance < payment.amount:
        return {"error": "Insufficient Balance"}

    # 5. Execute Transfer (Atomic)
    sender.balance -= payment.amount
    receiver.balance += payment.amount

    # 6. Record Transaction
    new_txn = Transaction(
        sender_id=sender.id,
        receiver_id=receiver.id,
        amount=payment.amount,
        status="SUCCESS",
        timestamp=datetime.datetime.now()
    )
    db.add(new_txn)

    # 7. Commit to DB
    db.commit()
    db.refresh(new_txn)

    return {"status": "SUCCESS", "transaction_id": new_txn.id, "new_balance": sender.balance}


def get_merchant_by_handle(db: Session, handle: str):
    return db.query(Merchant).filter(Merchant.handle == handle).first()

def get_merchant_history(db: Session, merchant_id: int):
    # Returns list of transactions where this merchant was the receiver
    return db.query(Transaction).filter(Transaction.receiver_id == merchant_id).all()