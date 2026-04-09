class DecisionEngine:
    def __init__(self, low_thresh=30, medium_thresh=60, high_thresh=85):
        self.low_thresh = low_thresh
        self.medium_thresh = medium_thresh
        self.high_thresh = high_thresh
        
    def get_decision(self, risk_score):
        """Returns decision based on score 0-100"""
        if risk_score < self.low_thresh:
            return "Approve"
        elif risk_score < self.medium_thresh:
            return "Ask OTP"
        elif risk_score < self.high_thresh:
            return "Manual Review"
        else:
            return "Block Transaction"
