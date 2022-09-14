from django.db import models
from django.contrib.auth.models import User
from django.db.models import ImageField
from django.urls import reverse
from PIL import Image

class Photo(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d', default='/media/profile_pics/ha.jpg')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    up = models.ManyToManyField(User, related_name='up_post', blank=True)
    down = models.ManyToManyField(User, related_name='down_post', blank=True)
    bookmark = models.ManyToManyField(User, related_name='bookmark_post', blank=True)
    
    def __str__(self):
        return "text : " +self.text
    
    class Meta:
        ordering = ['-created']
        
    def get_absolute_url(self):
        return reverse('photo:detail', args=[self.id])
    
class Comment(models.Model):
    #댓글 기능 구현을 위해 <작성자, 댓글 내용, 댓글 생성일, 댓글 수정일, 해당 사진>
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    photo = models.ForeignKey(Photo, null=True, blank=True, on_delete=models.CASCADE)
