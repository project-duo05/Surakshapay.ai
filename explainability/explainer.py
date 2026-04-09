import json

class Explainer:
    def generate_explanation(self, transaction, rule_reasons, anomaly_score, fraud_probability):
        reasons = list(rule_reasons)
        
        if anomaly_score > 0.7:
            reasons.append(f"High anomaly score detected ({anomaly_score:.2f})")
            
        if fraud_probability > 0.7:
            reasons.append(f"High fraud model probability ({fraud_probability:.2f})")
            
        transaction.explainability_reasons = json.dumps(reasons)
        return reasons
