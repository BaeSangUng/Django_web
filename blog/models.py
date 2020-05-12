from django.db import models
from django.contrib.auth.models import User
# Django already made object about User that I have specified as 'author'. I can check in the server/admin
# admin / 1234
# 모델이 수정 될때마다 python manage.py makemigration, python manage.py migrate

class Post(models.Model):
    title = models.CharField(max_length=30)     # 제목
    content = models.TextField()                # 내용

    head_image = models.ImageField(upload_to='blog/%Y/%m/%d', blank=True)   # pip install Pillow  - 이미지 추가, 년월일 별로

    created = models.DateTimeField()    # 작성 날짜
    author = models.ForeignKey(User, on_delete=models.CASCADE)    # 작성자 ,  on_delete = True : 회원 탈퇴시 django에 연결된 User도 삭제 할 것인지?  3.0 버전에서 True가 아니라 models.CASCADE로 바뀜

    def __str__(self):
        return '{} :: {}'.format(self.title, self.author)   # POST라는 객체를 표현될 때 어떻게 표현될 것인지

    def get_absolute_url(self):
        return '/blog/{}/'.format(self.pk)