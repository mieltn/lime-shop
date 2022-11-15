from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password']
        )
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_admin')
        extra_kwargs = {'password': {'write_only': True}}
        