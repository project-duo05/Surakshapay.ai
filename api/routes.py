from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from database.db import get_db
from database.models import User, Transaction, UserProfile, Alert
from api.schemas import TransactionRequest, RiskResponse, UserLogin, Token
from authentication.auth import verify_password, create_access_token
from rule_modules.engine import RuleEngine
from risk_modules.hybrid_scorer import HybridRiskEngine
from decision_modules.decision import DecisionEngine
from explainability.explainer import Explainer
from risk_modules.profiler import UserProfiler
from utils.alerts_manager import AlertManager
from utils.audit_logger import AuditLogger
import json

router = APIRouter()

rule_engine = RuleEngine()
hybrid_engine = HybridRiskEngine()
decision_engine = DecisionEngine()
explainer = Explainer()
profiler = UserProfiler()
alert_manager = AlertManager()
audit_logger = AuditLogger()

@router.post("/predict", response_model=RiskResponse)
def predict_fraud(req: TransactionRequest, db: Session = Depends(get_db)):
    try:
        # 1. Fetch or create user profile
        profile = db.query(UserProfile).filter(UserProfile.user_id == req.user_id).first()
        if not profile:
            profile = UserProfile(user_id=req.user_id)
            db.add(profile)
            db.commit()

        # 2. Create Transaction record
        txn = Transaction(
            transaction_id=req.transaction_id,
            user_id=req.user_id,
            amount=req.amount,
            location=req.location,
            merchant=req.merchant,
            timestamp=datetime.utcnow()
        )
        
        # 3. Profiling updates
        profiler.update_profile(db, profile, req.amount, txn.timestamp, req.location)
        
        # 4. Rule Engine
        rule_score, rule_reasons = rule_engine.evaluate(txn, profile)
        txn.rule_score = rule_score
        
        # 5. Mock AI logic (in a real scenario, use actual model inferences)
        import random
        txn.anomaly_score = random.uniform(0.0, 1.0)
        txn.fraud_probability = random.uniform(0.0, 1.0)
        
        # 6. Hybrid Risk Score
        txn.final_risk_score = hybrid_engine.calculate_risk_score(txn.anomaly_score, txn.fraud_probability, rule_score)
        
        # 7. Decision
        txn.decision = decision_engine.get_decision(txn.final_risk_score)
        
        # 8. Explainability
        reasons = explainer.generate_explanation(txn, rule_reasons, txn.anomaly_score, txn.fraud_probability)
        
        db.add(txn)
        db.commit()
        
        # 9. Alerts and Audit
        alert_manager.check_and_create_alert(db, txn)
        audit_logger.log_decision(db, txn, req.user_id, json.dumps(reasons))
        
        return RiskResponse(
            transaction_id=req.transaction_id,
            risk_score=txn.final_risk_score,
            decision=txn.decision,
            reasons=reasons
        )
    except Exception as e:
        import logging
        logging.error(f"Error processing transaction {req.transaction_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the transaction."
        )

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.is_resolved == False).all()
    return [{"id": a.id, "transaction": a.transaction_id, "score": a.risk_score, "msg": a.message} for a in alerts]
