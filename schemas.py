from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username:str
    full_name:str

class UserCreate(UserBase):
    pin:str
    balance: float=0.0

class UserResponse(UserBase):
    id:int
    balance: float
    class Config:
        from_attributes = True


class MerchantBase(BaseModel):
    handle: str
    full_name: str

class MerchantCreate(MerchantBase):
    balance: float = 0.0

class MerchantResponse(MerchantBase):
    id: int
    balance: float

    class Config:
        from_attributes = True

class PaymentRequest(BaseModel):
    receiver_handle: str
    amount: float
    pin: str

class TransactionResponse(BaseModel):
    transaction_id: int
    status: str
    amount: float
    timestamp: datetime

    class Config:
        from_attributes = True
