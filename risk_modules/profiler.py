from datetime import datetime

class UserProfiler:
    def __init__(self):
        pass

    def update_profile(self, db_session, user_profile, amount, transaction_time, location):
        """Updates user profile statistics based on the new transaction."""
        if user_profile.avg_transaction_amount == 0:
            user_profile.avg_transaction_amount = amount
        else:
            # Simple moving average approximation
            user_profile.avg_transaction_amount = (user_profile.avg_transaction_amount * 0.9) + (amount * 0.1)
            
        user_profile.last_transaction_time = transaction_time
        if user_profile.home_location == "Unknown":
            user_profile.home_location = location
            
        db_session.commit()
