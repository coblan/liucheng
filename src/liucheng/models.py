# encoding:utf-8

from __future__ import unicode_literals

from django.db import models

WORKNODE_STATUS=(
    ('waiting','等待'),
    ('working','处理中'),
    ('finish','完成'),
)
# Create your models here.
class WorkNode(models.Model):
    short_desp=models.CharField('简略描述',max_length=300,blank=True)
    long_desp=models.TextField('详细描述',blank=True)
    status=models.CharField('状态',max_length=30,default='waiting',choices=WORKNODE_STATUS)
    mtime=models.DateTimeField(verbose_name='修改时间',auto_now=True)
    