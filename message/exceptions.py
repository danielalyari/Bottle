from rest_framework.exceptions import ValidationError

class NotEnoughCoins(ValidationError):
    def __init__(self, detail="Not enough coins."):
        super().__init__({"detail": detail})