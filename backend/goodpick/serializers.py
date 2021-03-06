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
from .models import GoodsImage

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
    raise serializers.ValidationError("Thông tin đăng nhập không chính xác. Vui lòng thử lại.")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('goodsCategoryID', 'goodsCategoryName')

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = '__all__'

class GoodsSerializer(serializers.ModelSerializer):
    images = GoodsImageSerializer(source='goodsimage_set', many=True, read_only=True)

    class Meta:
        model = Goods
        fields = ('goodsID', 'goodsCreateId', 'goodsName', 'goodsCategoryID', 'goodsDescription', 'goodsPrice', 'goodsStatus', 'goodsLocation', 'goodsUpdatedTime', 'images')
    
    def create(self, validated_data):
        images = self.context.get('request').FILES
        goods = Goods.objects.create(
            goodsName=validated_data.get('goodsName'),
            goodsCategoryID=validated_data.get('goodsCategoryID'),
            goodsDescription=validated_data.get('goodsDescription', ''),
            goodsPrice=validated_data.get('goodsPrice'),
            goodsLocation=validated_data.get('goodsLocation', 'Hanoi'),
            goodsCreateId=validated_data.get('goodsCreateId'),
        )

        for index, image in enumerate(images.values()):
            isMain = str(index) == self.context.get('request').data.get('mainIndex')
            GoodsImage.objects.create(goodsID=goods, image=image, isMain=isMain)
        return goods

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
