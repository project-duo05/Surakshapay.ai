from database.models import Alert
from datetime import datetime

class AlertManager:
    def check_and_create_alert(self, db_session, transaction):
        """Creates an alert if the risk score is severely high."""
        if transaction.final_risk_score >= 85: # Very High Risk -> Block
            alert = Alert(
                transaction_id=transaction.transaction_id,
                risk_score=transaction.final_risk_score,
                message=f"CRITICAL: Blocked transaction {transaction.transaction_id} due to high risk ({transaction.final_risk_score:.1f})."
            )
            db_session.add(alert)
            db_session.commit()
            return alert
        return None
