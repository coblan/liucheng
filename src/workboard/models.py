# encoding:utf-8

from __future__ import unicode_literals

from django.db import models
import json
from helpers.base.jsonfield import JsonField
from helpers.case.organize.models import Employee

WORKNODE_STATUS=(
    ('waiting','等待'),
    ('finish','完成'),
)

#WORKGROUP_TYPE=(
    #('workrecord','记录'),
    #('template','模板'),
#)
class WorkGroup(models.Model):
    """
    代表一个流程
    """
    order=JsonField(verbose_name='进度详情',default=[],blank=True)
    
    short_desp=models.CharField('简略描述',max_length=300,blank=True)
    long_desp=models.TextField('详细描述',blank=True)
    client=models.ForeignKey('BusClient',verbose_name='客户',blank=True,null=True)
    #kind=models.CharField('类型',max_length=30,choices=WORKGROUP_TYPE,default='workrecord')
    create_time=models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    
    
    def __unicode__(self):
        return unicode(self.client) + '/' + self.short_desp
    
    class Meta:
        verbose_name="工作流程表"
        
        
    
# Create your models here.
class WorkNode(models.Model):
    short_desp=models.CharField('简略描述',max_length=300,blank=True)
    long_desp=models.TextField('详细描述',blank=True)
    status=models.CharField('状态',max_length=30,default='waiting',choices=WORKNODE_STATUS)
    create_time=models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    mtime=models.DateTimeField(verbose_name='修改时间',auto_now=True)
    work_group=models.ForeignKey(WorkGroup,verbose_name='工作流程',blank=True,null=True)
    owner=models.ForeignKey(Employee,verbose_name='负责人',blank=True,null=True,related_name='work_nodes')
    start_time=models.CharField('启动时间',max_length=20,blank=True)
    
    class Meta:
        verbose_name="工作步骤表"
    

class BusClient(models.Model):
    name=models.CharField('客户名称',max_length=200,blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name="客户信息表"

class WorkTemplate(models.Model):
    short_desp=models.CharField('简略描述',max_length=300,blank=True)
    long_desp=models.TextField('详细描述',blank=True)
    content=JsonField(verbose_name='内容',blank=True,default=[])
    
    
    

