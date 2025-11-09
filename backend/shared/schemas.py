from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Career Schemas
class CareerGoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    target_date: Optional[datetime] = None

class CareerGoalCreate(CareerGoalBase):
    pass

class CareerGoalResponse(CareerGoalBase):
    id: int
    user_id: int
    status: str
    progress_percentage: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Health Schemas
class HealthRecordBase(BaseModel):
    record_type: str
    value: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None

class HealthRecordCreate(HealthRecordBase):
    pass

class HealthRecordResponse(HealthRecordBase):
    id: int
    user_id: int
    recorded_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Finance Schemas
class FinancialTransactionBase(BaseModel):
    transaction_type: str
    category: str
    amount: float
    description: Optional[str] = None

class FinancialTransactionCreate(FinancialTransactionBase):
    pass

class FinancialTransactionResponse(FinancialTransactionBase):
    id: int
    user_id: int
    transaction_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# ML Recommendation Schemas
class MLRecommendationResponse(BaseModel):
    id: int
    user_id: int
    recommendation_type: str
    title: str
    description: str
    confidence_score: Optional[float] = None
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

