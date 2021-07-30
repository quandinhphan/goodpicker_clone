from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import User
from .models import Goods
from .models import Order
from .models import Rating
from .models import Comment
from .models import Chat
from .models import Category
from .models import ProductImage

#User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'userImage')

#Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'], validated_data['name'])

        return user

#Login Serializer
class LoginSerializer(serializers.Serializer):
  email = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    user = authenticate(**data)
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Incorrect Credentials")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('goodsCategoryID', 'goodsCategoryName')

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('goodsImageID', 'goodsImage1', 'goodsImage2', 'goodsImage3')

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('goodsID', 'goodsCreateId', 'goodsImageID', 'goodsName', 'goodsCategoryID', 'goodsDescription', 'goodsPrice',
                  'goodsStatus', 'goodsLocation', 'goodsUpdatedTime')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('userID', 'goodsID', 'orderStatus', 'orderTransactionTime')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('userID', 'goodsID', 'ratingScore')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('userID', 'goodsID', 'commentContent', 'commentTime')


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('userID', 'goodsID', 'chatContent', 'chatTime')
