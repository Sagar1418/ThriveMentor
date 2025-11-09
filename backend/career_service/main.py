from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from shared.database import get_db
from shared.models import User, CareerGoal, MLRecommendation
from shared.schemas import CareerGoalCreate, CareerGoalResponse, MLRecommendationResponse
from shared.auth import get_current_user
from shared.ml_service import generate_career_recommendations

app = FastAPI(title="ThriveMentor Career Service", version="1.0.0")

@app.post("/goals", response_model=CareerGoalResponse, status_code=status.HTTP_201_CREATED)
def create_career_goal(
    goal: CareerGoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new career goal"""
    db_goal = CareerGoal(
        user_id=current_user.id,
        title=goal.title,
        description=goal.description,
        target_date=goal.target_date,
        status="in_progress"
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    
    # Trigger ML recommendations after goal creation
    generate_career_recommendations(current_user.id, db)
    
    return db_goal

@app.get("/goals", response_model=List[CareerGoalResponse])
def get_career_goals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all career goals for current user"""
    goals = db.query(CareerGoal).filter(
        CareerGoal.user_id == current_user.id
    ).all()
    return goals

@app.get("/goals/{goal_id}", response_model=CareerGoalResponse)
def get_career_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific career goal"""
    goal = db.query(CareerGoal).filter(
        CareerGoal.id == goal_id,
        CareerGoal.user_id == current_user.id
    ).first()
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career goal not found"
        )
    return goal

@app.put("/goals/{goal_id}", response_model=CareerGoalResponse)
def update_career_goal(
    goal_id: int,
    goal: CareerGoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a career goal"""
    db_goal = db.query(CareerGoal).filter(
        CareerGoal.id == goal_id,
        CareerGoal.user_id == current_user.id
    ).first()
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career goal not found"
        )
    
    db_goal.title = goal.title
    db_goal.description = goal.description
    db_goal.target_date = goal.target_date
    db.commit()
    db.refresh(db_goal)
    return db_goal

@app.patch("/goals/{goal_id}/progress")
def update_goal_progress(
    goal_id: int,
    progress: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update progress percentage of a career goal"""
    db_goal = db.query(CareerGoal).filter(
        CareerGoal.id == goal_id,
        CareerGoal.user_id == current_user.id
    ).first()
    if not db_goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career goal not found"
        )
    
    db_goal.progress_percentage = min(max(progress, 0.0), 100.0)
    if db_goal.status == "in_progress" and db_goal.progress_percentage >= 100:
        db_goal.status = "completed"
    db.commit()
    return {"message": "Progress updated", "progress": db_goal.progress_percentage}

@app.get("/recommendations", response_model=List[MLRecommendationResponse])
def get_career_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get ML-powered career recommendations"""
    recommendations = db.query(MLRecommendation).filter(
        MLRecommendation.user_id == current_user.id,
        MLRecommendation.recommendation_type == "career"
    ).order_by(MLRecommendation.created_at.desc()).limit(10).all()
    return recommendations

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "career_service"}

