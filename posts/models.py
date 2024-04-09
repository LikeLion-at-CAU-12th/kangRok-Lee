from django.db import models
from config.settings import AUTH_USER_MODEL

# Create your models here.
class BaseModel(models.Model) :
    created_at = models.DateTimeField(verbose_name = "작성일시", auto_now_add = True)
    updated_at = models.DateTimeField(verbose_name = "수정일시", auto_now = True)
    # writer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Post(BaseModel) :
    CHOICES  = (
        ('DIARY', '일기'), #DB저장할실제값, 우리에게보이는이름
        ('STUDY', '공부'),
        ('ETC', '기타')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="제목", max_length=20)
    # writer : for testing purposes
    writer = models.CharField(max_length=20)
    content = models.TextField(verbose_name="내용")
    category = models.CharField(choices=CHOICES, max_length=20)

class Comment(BaseModel) :
    id = models.AutoField(primary_key=True)
    # writer : for testing purposes
    writer = models.CharField(max_length=20)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
