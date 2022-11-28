from django.db import models

# Create your models here.
class Feed(models.Model):
    content = models.TextField() # 글 내용
    image = models.TextField() # 피드 이미지
    email = models.EmailField(default='') # 이메일
    like_count    = models.IntegerField() # 좋아요 수
    # profile_image = models.TextField() # 프로필 이미지
    # user_id       = models.TextField() # 글쓴이

class Like(models.Model):
    feed_id = models.IntegerField(default=0) # 어떤 글을 좋아요 눌렀는지 알기 위해
    email = models.EmailField(default='') # 좋아요 누른 사람
    is_like = models.BooleanField(default=True) # 좋아요 눌렀는지

    # 1번 글에 좋아요 누르면
    # 1 tmddnjs513@naver.com Y
    # 취소하면 Y->N
    # write하고 update하는 방법 채택
    # write하고 delete하는 방법

class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    reply_content = models.TextField() # 댓글 내용

class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=False)

