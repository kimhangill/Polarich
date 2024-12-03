from rest_framework import serializers
from .models import Article, Challange, ArticleImage, Comment

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields= ('id','image','uploaded_at',)





        
        
class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    user_profileImage = serializers.ImageField(source='user.profileImage', read_only=True)
    class Meta:
        model = Comment
        fields = ('id','article','user','user_nickname','content','created_at','updated_at','user_profileImage',)
        read_only_fields=('user','created_at','updated_at','user_nickname','user_profileImage',)

class ArticleSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    user_profileImage = serializers.ImageField(source='user.profileImage', read_only=True)
    images = ArticleImageSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)  # 댓글 목록을 CommentSerializer를 사용해 가져옴

    class Meta:
        model = Article
        fields = ['id', 'user', 'user_nickname', 'title', 'content', 'created_at', 'images', 'updated_at', 'type', 'comments','user_profileImage']
        read_only_fields = ['user', 'created_at', 'updated_at', 'comments','user_profileImage']

class ArticleListSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'user', 'user_nickname', 'title', 'created_at', 'updated_at', 'type', 'comment_count']
        read_only_fields = ('user', 'created_at', 'updated_at')

    def get_comment_count(self, obj):
        return obj.comments.count()
