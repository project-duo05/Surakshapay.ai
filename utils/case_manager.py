from database.models import Case
from datetime import datetime

class CaseManager:
    def open_case(self, db_session, transaction_id):
        """Opens a new investigation case for a transaction."""
        new_case = Case(
            transaction_id=transaction_id,
            status="Open",
            fraud_label="Pending"
        )
        db_session.add(new_case)
        db_session.commit()
        return new_case
        
    def resolve_case(self, db_session, case_id, analyst_id, fraud_label, notes):
        """Resolves an existing case."""
        case = db_session.query(Case).filter(Case.id == case_id).first()
        if case:
            case.analyst_id = analyst_id
            case.fraud_label = fraud_label
            case.notes = notes
            case.status = "Closed"
            case.closed_at = datetime.utcnow()
            db_session.commit()
            return case
        return None
