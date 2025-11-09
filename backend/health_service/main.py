from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from shared.database import get_db
from shared.models import User, HealthRecord, MLRecommendation
from shared.schemas import HealthRecordCreate, HealthRecordResponse, MLRecommendationResponse
from shared.auth import get_current_user
from shared.ml_service import generate_health_recommendations

app = FastAPI(title="ThriveMentor Health Service", version="1.0.0")

@app.post("/records", response_model=HealthRecordResponse, status_code=status.HTTP_201_CREATED)
def create_health_record(
    record: HealthRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new health record"""
    db_record = HealthRecord(
        user_id=current_user.id,
        record_type=record.record_type,
        value=record.value,
        unit=record.unit,
        notes=record.notes
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    # Trigger ML recommendations after record creation
    generate_health_recommendations(current_user.id, db)
    
    return db_record

@app.get("/records", response_model=List[HealthRecordResponse])
def get_health_records(
    record_type: str = None,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health records for current user"""
    query = db.query(HealthRecord).filter(
        HealthRecord.user_id == current_user.id
    )
    
    if record_type:
        query = query.filter(HealthRecord.record_type == record_type)
    
    # Filter by date range
    start_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(HealthRecord.recorded_at >= start_date)
    
    records = query.order_by(HealthRecord.recorded_at.desc()).all()
    return records

@app.get("/records/{record_id}", response_model=HealthRecordResponse)
def get_health_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific health record"""
    record = db.query(HealthRecord).filter(
        HealthRecord.id == record_id,
        HealthRecord.user_id == current_user.id
    ).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health record not found"
        )
    return record

@app.get("/analytics/summary")
def get_health_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health analytics summary"""
    # Get records from last 30 days
    start_date = datetime.utcnow() - timedelta(days=30)
    records = db.query(HealthRecord).filter(
        HealthRecord.user_id == current_user.id,
        HealthRecord.recorded_at >= start_date
    ).all()
    
    # Calculate basic statistics
    summary = {}
    for record in records:
        if record.record_type not in summary:
            summary[record.record_type] = {
                "count": 0,
                "total": 0,
                "average": 0,
                "unit": record.unit
            }
        summary[record.record_type]["count"] += 1
        if record.value:
            summary[record.record_type]["total"] += record.value
    
    # Calculate averages
    for record_type in summary:
        if summary[record_type]["count"] > 0:
            summary[record_type]["average"] = (
                summary[record_type]["total"] / summary[record_type]["count"]
            )
    
    return summary

@app.get("/recommendations", response_model=List[MLRecommendationResponse])
def get_health_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get ML-powered health recommendations"""
    recommendations = db.query(MLRecommendation).filter(
        MLRecommendation.user_id == current_user.id,
        MLRecommendation.recommendation_type == "health"
    ).order_by(MLRecommendation.created_at.desc()).limit(10).all()
    return recommendations

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "health_service"}

