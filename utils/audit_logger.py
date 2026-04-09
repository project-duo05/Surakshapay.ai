from database.models import AuditLog
from datetime import datetime

class AuditLogger:
    def log_decision(self, db_session, transaction, user_id, reason, model_version="1.0.0"):
        """Logs every decision to the audit trace."""
        log = AuditLog(
            transaction_id=transaction.transaction_id,
            user_id=user_id,
            risk_score=transaction.final_risk_score,
            decision=transaction.decision,
            reason=reason,
            model_version=model_version
        )
        db_session.add(log)
        db_session.commit()
        return log
