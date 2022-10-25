from django.contrib.auth import get_user_model

from rest_framework import serializers
USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model"""
    class Meta:
        model = USER
        fields = ['email', 'phone', 'name' ]
        extra_kwargs = { # a dict to provide extra meta data 
            'password': 
                    {
                        'write_only': True, 
                        'min_length': 4
                    }
                        }
    def create(self, validated_data): 
        return USER.objects.create_user(**validated_data)

