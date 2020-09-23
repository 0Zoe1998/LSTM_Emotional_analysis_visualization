from django.db import models

# Create your models here.

class Notice(models.Model):
    title=models.CharField(u'标题',max_length=100)
    content=models.TextField(u'公告内容')
    pic_front=models.TextField(u'轮播图片地址',max_length=100,null=True,blank=True)
    pic_background=models.CharField(u'公告背景图地址',max_length=100,null=True,blank=True)
    public=models.BooleanField(u'公告展示',default=False)
    pic_mark=models.CharField(u'标记内容',max_length=100,null=True,blank=True)