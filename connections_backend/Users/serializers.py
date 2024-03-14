from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],            
        )
    
    class Meta:
        model = get_user_model()
        fields  = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password' : {'write_only': True}}

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    id = serializers.CharField(max_length = 15, read_only = True)
    password =  serializers.CharField(max_length = 255, write_only = True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError("An email address is required for login")
        if password is None:
            raise serializers.ValidationError("A password is required for login")
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        
        return {
            "email": user.email,
            "id": user.id

        }