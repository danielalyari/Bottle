from django.db import models
from django.contrib.auth.models import User
from message.exceptions import NotEnoughCoins


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=100)
    is_banned = models.BooleanField(default=False)

    def decrease_coins(self, amount: int):
        if self.coins < amount:
            raise NotEnoughCoins()
        self.coins -= amount
        self.save(update_fields=["coins"])


class Friend(models.Model):
    from_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('from_user', 'to_user')