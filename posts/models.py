from django.db import models
from config.settings import AUTH_USER_MODEL
from django.core.files.storage import default_storage

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
    # image = models.ImageField(verbose_name="사진 첨부", upload_to='images/', null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, verbose_name="썸네일")

    def save(self, *args, **kwargs):
        file = self.thumbnail
        if file:
            self.thumbnail = default_storage.url(file.name) #default_storage points to our S3
        super().save(*args, **kwargs)

    """
    TODO: fix
    response에서
    "https://qwertycvbnm.s3.ap-northeast-2.amazonaws.com/https%3A/qwertycvbnm.s3.ap-northeast-2.amazonaws.com/quokka.webp"
    와 같이 default.storage 값이 두번 중복되어 옴
    """    

    """
    ++DB에 URL 저장하지 않고 썸네일 전체URL 사용하기
    @property
    def thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        else:
            return None
    """

class Comment(BaseModel) :
    id = models.AutoField(primary_key=True)
    # writer : for testing purposes
    writer = models.CharField(max_length=20)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
