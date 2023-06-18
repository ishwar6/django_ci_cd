from django.contrib.auth import get_user_model, authenticate

from django.utils.translation import gettext as _ #common syntax for doing translation with django. 



from rest_framework import serializers
USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model"""
    class Meta:
        model = USER
        fields = ['email', 'password', 'name']
        extra_kwargs = { # a dict to provide extra meta data 
            'password': 
                    {
                        'write_only': True, 
                        'min_length': 10
                    }
                        }
    def create(self, validated_data): 
        "create user with validated data"
        return USER.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
