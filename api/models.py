from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    It overrides email to set it to unique and to convert it to the username_field
    """
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']


class Wallet(models.Model):
    """
    Wallet for managing money and transfers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.FloatField()


class Transfer(models.Model):
    """
    This model saves transfer history, in a future it should contain the state of the transfer because it could
    fail, it could be wrong, from_user may not contain enough balance, etc.
    """
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    amount = models.FloatField()

    @classmethod
    def create(cls, from_user, to_user, amount):
        from_user = User.objects.get(id=from_user)
        to_user = User.objects.get(id=to_user)
        to_user.wallet.balance += float(amount)
        from_user.wallet.balance -= float(amount)
        to_user.wallet.save()
        from_user.wallet.save()
        transfer = cls(from_user=from_user, to_user=to_user, amount=amount)
        return transfer