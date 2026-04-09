class DecisionEngine:
    """
    Maps final risk scores systematically to banking actions using dynamic percentile thresholds.
    """
    
    @staticmethod
    def get_decision(risk_score, p70=30.0, p90=60.0, p98=80.0):
        """
        Dynamic Threshold Rules based on training percentiles:
        * < 70th percentile → Approve Transaction
        * 70–90th percentile → Ask OTP Verification
        * 90–98th percentile → Flag for Manual Review
        * > 98th percentile → Block Transaction
        """
        if risk_score < p70:
            return "Approve Transaction", "low", "green"
        elif risk_score < p90:
            return "Ask OTP Verification", "medium", "orange"
        elif risk_score < p98:
            return "Flag for Manual Review", "high", "darkorange"
        else:
            return "Block Transaction", "critical", "red"

    @staticmethod
    def generate_human_explanation(transaction, risk_score, decision, reasons, model_top_features=None):
        exp = []
        if decision == "Approve Transaction":
            exp.append("Transaction conforms to user baselines and population norms.")
        else:
            exp.append(f"Flagged for {decision} due to an elevated risk score ({risk_score:.1f}/100).")
            
        if any(r != "No suspicious rules triggered." for r in reasons):
            exp.append("\nKey Behaviors Detected:")
            for r in reasons:
                if r != "No suspicious rules triggered.":
                    exp.append(f"- {r}")
                    
        if model_top_features and risk_score > max(30, risk_score * 0.5): # General cutoff logic for display
            exp.append("\nTop Model Discrepancies:")
            for feature, weight in model_top_features[:2]:
                exp.append(f"- {feature.replace('_', ' ').title()}")
                
        return "\n".join(exp)
