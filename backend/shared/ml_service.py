"""
ML Service for generating recommendations
This is a simplified ML service. In production, you would integrate
with more sophisticated ML models (TensorFlow, PyTorch, etc.)
"""
from sqlalchemy.orm import Session
from shared.models import (
    User, CareerGoal, HealthRecord, FinancialTransaction, MLRecommendation
)
from datetime import datetime, timedelta
import random

def generate_career_recommendations(user_id: int, db: Session):
    """Generate career recommendations based on user goals"""
    goals = db.query(CareerGoal).filter(
        CareerGoal.user_id == user_id,
        CareerGoal.status == "in_progress"
    ).all()
    
    if not goals:
        return
    
    # Simple recommendation logic (replace with actual ML model)
    recommendations = [
        {
            "title": "Update Your LinkedIn Profile",
            "description": "Based on your career goals, consider updating your LinkedIn profile to highlight relevant skills.",
            "confidence_score": 0.85
        },
        {
            "title": "Take an Online Course",
            "description": "Consider enrolling in courses related to your career goals to enhance your skills.",
            "confidence_score": 0.78
        }
    ]
    
    # Check if recommendation already exists
    existing = db.query(MLRecommendation).filter(
        MLRecommendation.user_id == user_id,
        MLRecommendation.recommendation_type == "career"
    ).first()
    
    if not existing:
        for rec in recommendations:
            db_rec = MLRecommendation(
                user_id=user_id,
                recommendation_type="career",
                title=rec["title"],
                description=rec["description"],
                confidence_score=rec["confidence_score"]
            )
            db.add(db_rec)
        db.commit()

def generate_health_recommendations(user_id: int, db: Session):
    """Generate health recommendations based on user records"""
    # Get recent health records
    start_date = datetime.utcnow() - timedelta(days=7)
    records = db.query(HealthRecord).filter(
        HealthRecord.user_id == user_id,
        HealthRecord.recorded_at >= start_date
    ).all()
    
    if not records:
        recommendations = [
            {
                "title": "Start Tracking Your Health",
                "description": "Begin logging your daily activities to get personalized health insights.",
                "confidence_score": 0.90
            }
        ]
    else:
        # Analyze records and generate recommendations
        recommendations = [
            {
                "title": "Maintain Consistent Exercise",
                "description": "You've been tracking your exercise. Keep up the consistency for better results!",
                "confidence_score": 0.82
            },
            {
                "title": "Monitor Your Sleep Patterns",
                "description": "Tracking your sleep can help identify patterns and improve your rest quality.",
                "confidence_score": 0.75
            }
        ]
    
    # Check if recommendation already exists
    existing = db.query(MLRecommendation).filter(
        MLRecommendation.user_id == user_id,
        MLRecommendation.recommendation_type == "health",
        MLRecommendation.created_at >= start_date
    ).first()
    
    if not existing:
        for rec in recommendations:
            db_rec = MLRecommendation(
                user_id=user_id,
                recommendation_type="health",
                title=rec["title"],
                description=rec["description"],
                confidence_score=rec["confidence_score"]
            )
            db.add(db_rec)
        db.commit()

def generate_finance_recommendations(user_id: int, db: Session):
    """Generate financial recommendations based on user transactions"""
    # Get recent transactions
    start_date = datetime.utcnow() - timedelta(days=30)
    transactions = db.query(FinancialTransaction).filter(
        FinancialTransaction.user_id == user_id,
        FinancialTransaction.transaction_date >= start_date
    ).all()
    
    if not transactions:
        recommendations = [
            {
                "title": "Start Tracking Your Expenses",
                "description": "Begin logging your financial transactions to get insights into your spending habits.",
                "confidence_score": 0.90
            }
        ]
    else:
        # Calculate spending patterns
        total_expenses = sum(
            t.amount for t in transactions if t.transaction_type == "expense"
        )
        total_income = sum(
            t.amount for t in transactions if t.transaction_type == "income"
        )
        
        recommendations = []
        if total_expenses > total_income * 0.8:
            recommendations.append({
                "title": "Consider Budgeting",
                "description": "Your expenses are high relative to income. Consider creating a budget to manage spending better.",
                "confidence_score": 0.88
            })
        
        if total_income > 0 and len([t for t in transactions if t.transaction_type == "investment"]) == 0:
            recommendations.append({
                "title": "Start Investing",
                "description": "Consider allocating a portion of your income to investments for long-term growth.",
                "confidence_score": 0.80
            })
        
        if not recommendations:
            recommendations.append({
                "title": "Review Your Financial Goals",
                "description": "Regularly review your financial transactions to stay on track with your goals.",
                "confidence_score": 0.70
            })
    
    # Check if recommendation already exists
    existing = db.query(MLRecommendation).filter(
        MLRecommendation.user_id == user_id,
        MLRecommendation.recommendation_type == "finance",
        MLRecommendation.created_at >= start_date
    ).first()
    
    if not existing:
        for rec in recommendations:
            db_rec = MLRecommendation(
                user_id=user_id,
                recommendation_type="finance",
                title=rec["title"],
                description=rec["description"],
                confidence_score=rec["confidence_score"]
            )
            db.add(db_rec)
        db.commit()

