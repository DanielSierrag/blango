from rest_framework import serializers
from blango_auth.models import User
from blog.models import Post, Tag, Comment


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email']


class CommentSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(required=False)
  creator = UserSerializer(read_only=True)

  class Meta:
    model = Comment
    fields = ["id", "creator", "content", "modified_at", "created_at"]
    readonly = ['modified_at', 'created_at']


class TagField(serializers.SlugRelatedField):
  def to_internal_value(self, data):
    try:
      return self.get_queryset().get_or_create(value=data.lower())[0]
    except (ValueError, TypeError):
      self.fail(f"Tag value {data} is invalid")


class PostSerializer(serializers.ModelSerializer):
  tags = TagField(
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


class PostDetailSerializer(PostSerializer):
  comments = CommentSerializer(many=True)

  def update(self, instance, validated_data):
    comments = validated_data.pop("comments")

    instance = super(PostDetailSerializer, self).update(instance, validated_data)

    for comment_data in comments:
      if comment_data.get('id'):
        # We infer comments with id are pre-existing
        continue
      
      # Create comment instance if doesn't have id
      comment = Comment(**comment_data)
      comment.creator = self.context['request'].user
      comment.content_object = instance
      comment.save()
      
    return instance