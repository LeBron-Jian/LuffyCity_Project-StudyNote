# by gaoxin
from rest_framework import serializers
from Course.models import Account
import hashlib


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = "__all__"

    def create(self, validated_data):
        pwd = validated_data["pwd"]
        pwd_salt = "luffy_password" + pwd
        md5_str = hashlib.md5(pwd_salt.encode()).hexdigest()
        user_obj = Account.objects.create(username=validated_data["username"], pwd=md5_str)
        return user_obj