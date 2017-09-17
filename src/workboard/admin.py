# encoding:utf-8

from django.contrib import admin
from helpers.director.shortcut import ModelTable,TablePage,page_dc
from .models import WorkGroup
# Register your models here.
class WorkGroupPage(TablePage):
    class WorkGroupTable(ModelTable):
        model=WorkGroup
        exclude=[]
    
    tableCls=WorkGroupTable

page_dc.update({
    'workboard.workgroup':WorkGroupPage,
})


