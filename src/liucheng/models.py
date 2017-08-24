# encoding:utf-8

from __future__ import unicode_literals

from django.db import models

WORKNODE_STATUS=(
    ('waiting','等待'),
    ('working','处理中'),
    ('finish','完成'),
)

class NodeGroup(models.Model):
    relations=models.TextField(verbose_name='节点关系',blank=True)
# Create your models here.
class WorkNode(models.Model):
    short_desp=models.CharField('简略描述',max_length=300,blank=True)
    long_desp=models.TextField('详细描述',blank=True)
    status=models.CharField('状态',max_length=30,default='waiting',choices=WORKNODE_STATUS)
    mtime=models.DateTimeField(verbose_name='修改时间',auto_now=True)
    node_group=models.ForeignKey(NodeGroup,verbose_name='节点组',blank=True,null=True)
    client=models.ForeignKey('BusClient',verbose_name='客户',blank=True,null=True)

class BusClient(models.Model):
    name=models.CharField('客户名称',max_length=200,blank=True)
    
    def __unicode__(self):
        return self.name


