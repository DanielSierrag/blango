from rest_framework import serializers
from blango_auth.models import User
from blog.models import Post, Tag

class PostSerializer(serializers.ModelSerializer):
  tags = serializers.SlugRelatedField(
    slug_field='value',
    queryset=Tag.objects.all(),
    many=True
  )
  author = serializers.HyperlinkedRelatedField(
    queryset=User.objects.all(),
    lookup_field='email',
    view_name='api_user_detail'
  )
  class Meta:
    model = Post
    fields = '__all__'
    readonly = ['created_at', 'modified_at']


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email']