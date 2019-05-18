from rest_framework import serializers
from .models import User, Wallet, Transfer


class WalletSerializer(serializers.ModelSerializer):
    """
    Wallet serializer, just serializes balance
    """
    class Meta:
        model = Wallet
        fields = ('balance', )


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer, it serializes user data along with wallet
    """
    wallet = WalletSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'username', 'wallet')
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        """
        Create method is inherited so that we can save the password as a hash instead of plain data, also it allows us
        to create a wallet along the user with a default 10 balance
        :param validated_data:
        :return: user
        """
        password = validated_data.pop('password')
        wallet = validated_data.pop('wallet')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Any user can create a wallet with a custom initial balance, this is to speed up development and tests
        Wallet.objects.create(user=user, **wallet)

        return user


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('from_user', 'to_user', 'amount')
