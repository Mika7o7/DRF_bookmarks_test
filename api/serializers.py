from rest_framework import serializers
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .bookmark_service.utils import extract_metadata
from .models import (
    User,
    Collection,
    Bookmark,
)


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * email
      * password.
    It will try to authenticate the user with when validated.
    """

    email = serializers.EmailField(label="Email", write_only=True)
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        # Take email and password from request
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = "Access denied: wrong email or password."
                raise serializers.ValidationError(msg, code="authorization")
            
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code="authorization")
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs["user"] = user
        return attrs



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )


    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
        )
    
        user.set_password(validated_data["password"])
        user.save()

        return user



class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "name", "description", 'created_at', 'updated_at']


    def create(self, validated_data):
        user = validated_data['user']
        name = validated_data['name']
        description = validated_data['description']

        collection = Collection.objects.create(
            user=user,
            description=description,
            name=name,
        )

        return collection
    


class BookmarkSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = Bookmark
        fields = ['id', 'title', 'description', 'link', 'type', 'image_preview', 'created_at', 'updated_at', 'collection']


class BookmarkCreateSerializer(serializers.Serializer):
    link = serializers.URLField()
    type = serializers.ChoiceField(choices=['website', 'book', 'article', 'music', 'video'])
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all(), default=None)
    

    def create(self, validated_data):
        link = validated_data['link']
        bookmark_type = validated_data['type']
        user = validated_data['user']
        collection = validated_data['collection']
        # Extract metadata from the link
        metadata = extract_metadata(link)

        # Assuming you have a Bookmark model, create a new instance
        bookmark = Bookmark.objects.create(
            user=user,
            title=metadata.get('title', ''),
            description=metadata.get('description', ''),
            link=link,
            type=bookmark_type,
            image_preview=metadata.get('image', ''),
            collection=Collection.objects.get(pk=int(collection)),
        )

        return bookmark

