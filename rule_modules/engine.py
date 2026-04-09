from datetime import datetime

class RuleEngine:
    def evaluate(self, transaction, user_profile):
        """
        Evaluates a transaction against business rules and returns a score 0-100.
        """
        score = 0
        reasons = []

        if transaction.amount > 50000:
            score += 30
            reasons.append("Amount exceeds 50000")
            transaction.high_amount_flag = True
            
        if user_profile and user_profile.avg_transaction_amount > 0:
            if transaction.amount > 3 * user_profile.avg_transaction_amount:
                score += 30
                reasons.append("Amount is 3x higher than user average")
                transaction.high_amount_flag = True
                
        # Night transaction (12 AM to 5 AM)
        hour = transaction.timestamp.hour
        if 0 <= hour <= 5:
            score += 20
            reasons.append("Transaction occurred during unusual hours (12AM - 5AM)")
            transaction.unusual_time_flag = True
            
        if user_profile and transaction.location != user_profile.home_location:
            score += 20
            reasons.append("Transaction occurred in a new location")
            transaction.new_location_flag = True
            
        # Cap score at 100
        score = min(score, 100)
        return score, reasons
