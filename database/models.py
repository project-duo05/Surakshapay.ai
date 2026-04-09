from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # Admin, Fraud Analyst, Viewer

class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(Integer, primary_key=True, index=True)
    avg_transaction_amount = Column(Float, default=0.0)
    avg_transactions_per_day = Column(Float, default=0.0)
    usual_transaction_hour = Column(Integer, default=12)
    home_location = Column(String, default="Unknown")
    last_transaction_time = Column(DateTime, default=datetime.utcnow)
    transaction_velocity = Column(Float, default=0.0)

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String)
    merchant = Column(String)
    
    # Flags populated by risk engine
    unusual_time_flag = Column(Boolean, default=False)
    new_location_flag = Column(Boolean, default=False)
    high_amount_flag = Column(Boolean, default=False)
    
    # Scores
    anomaly_score = Column(Float, default=0.0)
    fraud_probability = Column(Float, default=0.0)
    rule_score = Column(Float, default=0.0)
    final_risk_score = Column(Float, default=0.0)
    
    # Decisions & Explainability
    decision = Column(String)
    explainability_reasons = Column(Text, default="[]") # JSON list
    
class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.transaction_id"))
    risk_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(String)
    is_resolved = Column(Boolean, default=False)
    
    transaction = relationship("Transaction")

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.transaction_id"))
    analyst_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="Open") # Open, Closed
    fraud_label = Column(String, default="Pending") # Fraud, Safe
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    transaction_id = Column(String, index=True)
    user_id = Column(Integer)
    risk_score = Column(Float)
    decision = Column(String)
    reason = Column(Text)
    model_version = Column(String)

class ModelMetric(Base):
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    fraud_detection_rate = Column(Float)
    data_drift_detected = Column(Boolean, default=False)
