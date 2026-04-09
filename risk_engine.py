class RiskEngine:
    @staticmethod
    def evaluate_rules(transaction):
        rule_score = 0
        reasons = []
        
        amount = transaction.get('amount', 0)
        if amount > 5000:
            rule_score += 50
            reasons.append(f"Extremely high amount (${amount:.2f})")
        elif amount > 2000:
            rule_score += 25
            reasons.append(f"High amount (${amount:.2f})")
            
        if transaction.get('night_transaction_flag', 0) == 1:
            rule_score += 25
            reasons.append("Late night transaction (12 AM - 5 AM)")
            
        if transaction.get('velocity', 0) > 0.1:
            rule_score += 20
            reasons.append("High transaction velocity detected")
            
        if transaction.get('unusual_amount_flag', 0) == 1:
            rule_score += 30
            reasons.append("Amount severely deviates from user average")
            
        rule_score = min(rule_score, 100)
        if not reasons:
            reasons.append("No suspicious rules triggered.")
            
        return float(rule_score), reasons

    @staticmethod
    def calculate_risk_score(anomaly_score, fraud_probability, rule_score):
        """
        Risk Score = 0.4 * anomaly_score + 0.4 * fraud_probability + 0.2 * rule_score
        All scaled strictly 0-100.
        """
        an = min(max(float(anomaly_score), 0), 100)
        fp = min(max(float(fraud_probability), 0), 100)
        rs = min(max(float(rule_score), 0), 100)
        
        final_score = (0.4 * an) + (0.4 * fp) + (0.2 * rs)
        return min(final_score, 100)
