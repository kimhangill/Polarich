from django.db import models
from django.conf import settings

class Article(models.Model):

    ARTICLE_TYPES = [
        ('general', 'General'),
        ('column', 'Professional Column'),
        ('qna', 'Q&A')
    ]

    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=ARTICLE_TYPES, default='general')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    # image = models.ImageField(upload_to='images/%Y-%m/',blank=True,null=True)

#이미지를 여러 장 넣을 필요가 있다면 IMAGE 모델을 하나 더 만들어 왜래키로 적용하는 게 합리적이라는 챗GPT 의견
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.article.title}"
#추후 구현 예정


#챌린지 게시판
class Challange(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participation = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="participate")
    title=models.CharField(max_length=100)
    content=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    
    def __str__(self):
        return f"{self.title} (hosted by {self.host.username})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date > self.end_date:
            raise ValidationError('Start date cannot be after end date.')

    class Meta:
        ordering = ['start_date']
        
#코멘트 모델
class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.nickname} 번 게시글 코멘트, 작성자:{self.article.title}"