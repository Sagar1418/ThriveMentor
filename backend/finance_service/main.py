from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from shared.database import get_db
from shared.models import User, FinancialTransaction, MLRecommendation
from shared.schemas import FinancialTransactionCreate, FinancialTransactionResponse, MLRecommendationResponse
from shared.auth import get_current_user
from shared.ml_service import generate_finance_recommendations

app = FastAPI(title="ThriveMentor Finance Service", version="1.0.0")

@app.post("/transactions", response_model=FinancialTransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: FinancialTransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new financial transaction"""
    db_transaction = FinancialTransaction(
        user_id=current_user.id,
        transaction_type=transaction.transaction_type,
        category=transaction.category,
        amount=transaction.amount,
        description=transaction.description
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Trigger ML recommendations after transaction creation
    generate_finance_recommendations(current_user.id, db)
    
    return db_transaction

@app.get("/transactions", response_model=List[FinancialTransactionResponse])
def get_transactions(
    transaction_type: str = None,
    category: str = None,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get financial transactions for current user"""
    query = db.query(FinancialTransaction).filter(
        FinancialTransaction.user_id == current_user.id
    )
    
    if transaction_type:
        query = query.filter(FinancialTransaction.transaction_type == transaction_type)
    if category:
        query = query.filter(FinancialTransaction.category == category)
    
    # Filter by date range
    start_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(FinancialTransaction.transaction_date >= start_date)
    
    transactions = query.order_by(FinancialTransaction.transaction_date.desc()).all()
    return transactions

@app.get("/transactions/{transaction_id}", response_model=FinancialTransactionResponse)
def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific financial transaction"""
    transaction = db.query(FinancialTransaction).filter(
        FinancialTransaction.id == transaction_id,
        FinancialTransaction.user_id == current_user.id
    ).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction

@app.get("/analytics/summary")
def get_financial_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get financial analytics summary"""
    # Get transactions from last 30 days
    start_date = datetime.utcnow() - timedelta(days=30)
    transactions = db.query(FinancialTransaction).filter(
        FinancialTransaction.user_id == current_user.id,
        FinancialTransaction.transaction_date >= start_date
    ).all()
    
    # Calculate summary
    total_income = sum(
        t.amount for t in transactions if t.transaction_type == "income"
    )
    total_expenses = sum(
        t.amount for t in transactions if t.transaction_type == "expense"
    )
    total_investments = sum(
        t.amount for t in transactions if t.transaction_type == "investment"
    )
    net_balance = total_income - total_expenses - total_investments
    
    # Category breakdown
    category_breakdown = {}
    for transaction in transactions:
        if transaction.transaction_type == "expense":
            if transaction.category not in category_breakdown:
                category_breakdown[transaction.category] = 0
            category_breakdown[transaction.category] += transaction.amount
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_investments": total_investments,
        "net_balance": net_balance,
        "category_breakdown": category_breakdown,
        "period_days": 30
    }

@app.get("/recommendations", response_model=List[MLRecommendationResponse])
def get_finance_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get ML-powered financial recommendations"""
    recommendations = db.query(MLRecommendation).filter(
        MLRecommendation.user_id == current_user.id,
        MLRecommendation.recommendation_type == "finance"
    ).order_by(MLRecommendation.created_at.desc()).limit(10).all()
    return recommendations

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "finance_service"}

