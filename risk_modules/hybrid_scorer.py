class HybridRiskEngine:
    def __init__(self, anomaly_weight=0.4, fraud_prob_weight=0.4, rule_weight=0.2):
        self.w_anomaly = anomaly_weight
        self.w_prob = fraud_prob_weight
        self.w_rule = rule_weight
        
    def calculate_risk_score(self, anomaly_score_norm, fraud_probability, rule_score_norm):
        """
        Inputs: normalized anomaly_score (0-1), fraud_probability (0-1), rule score (0-100)
        """
        hybrid_score = (
            (anomaly_score_norm * self.w_anomaly) + 
            (fraud_probability * self.w_prob) + 
            ((rule_score_norm / 100.0) * self.w_rule)
        )
        return hybrid_score * 100.0 # Return as 0-100
