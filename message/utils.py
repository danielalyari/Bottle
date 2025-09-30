from user.models import UserProfile


def decrease_coins(profile: UserProfile, amount: int) -> bool:
    if profile.coins < amount:
        return False
    profile.coins -= amount
    profile.save(update_fields=["coins"])
    return True