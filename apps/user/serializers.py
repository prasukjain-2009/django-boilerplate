from django.contrib.auth import authenticate, user_logged_in

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler

from .models import User


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    initials = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'initials', 'full_name', 'email', 'created')

    def get_full_name(self, obj):
        full_name = obj.first_name + " " + obj.last_name
        if full_name.strip():
           return full_name
        return obj.username

    def get_created(self, obj):
        return obj.date_joined.timestamp()

    def get_initials(self, obj):
        first_name_intial = obj.first_name[0].upper() if obj.first_name else ''
        last_name_intial = obj.last_name[0].upper() if obj.last_name else ''
        return first_name_intial+last_name_intial


class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        print("here")
        print(type(self),self.username_field)
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(request=self.context['request'], **credentials)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
