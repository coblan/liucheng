# encoding:utf-8

from django.contrib import admin
from helpers.director.shortcut import ModelTable,TablePage,page_dc,FormPage,ModelFields,model_dc,RowSort
from helpers.director.db_tools import permit_to_dict
from .models import WorkGroup,BusClient,WorkNode
# Register your models here.
class WorkGroupPage(TablePage):
    template='workboard/workboard.html'
    class WorkGroupTable(ModelTable):
        model=WorkGroup
        exclude=[]
        
        def dict_row(self, inst):

            return {
                "client":unicode(inst.client) if inst.client else "",
                "nodes":[permit_to_dict(self.crt_user,x) for x in  inst.worknode_set.order_by('id')]
                }
    
    tableCls=WorkGroupTable

class WorkGroupFormPage(FormPage):
    class WorkGroupForm(ModelFields):
        class Meta:
            model=WorkGroup
            exclude=[]
        def get_heads(self):
            heads= super(self.__class__,self).get_heads()
            heads=[x for x in heads if x['name'] != 'order']
            return heads
        
    fieldsCls=WorkGroupForm

class WorkNodeFormPage(FormPage):
    class WrokNodeForm(ModelFields):
        class Meta:
            model=WorkNode
            exclude=[]
        def dict_head(self, head):
            if head['name']=="start_time":
                head['type']='date'
            return head
    fieldsCls=WrokNodeForm

class ClientPage(TablePage):
    class ClientSort(RowSort):
        names=['name']
        def get_query(self, query):
            if self.sort_str:
                ls=self.sort_str.replace('name','converted').split(',')
                query= query.extra(select={'converted': 'CONVERT(name USING gbk)'},order_by=['converted'])
                return query.order_by(*ls)
            else:
                return query
            
            return 
    
    class ClientTabel(ModelTable):
        model=BusClient
    ClientTabel.sort=ClientSort
    tableCls=ClientTabel
    
    
class ClientFormPage(FormPage):
    class ClientForm(ModelFields):
        class Meta:
            model=BusClient
            exclude=[]
        def clean_name(self):
            name = self.cleaned_data.get('name')
            if BusClient.objects.filter(name=name):
                raise forms.ValidationError('公司名字重复')
            return name
    fieldsCls = ClientForm

model_dc[BusClient]={'fields':ClientFormPage.ClientForm}
model_dc[WorkGroup]={'fields':WorkGroupFormPage.WorkGroupForm}
model_dc[WorkNode]={'fields':WorkNodeFormPage.WrokNodeForm}

page_dc.update({
    'workboard.workgroup':WorkGroupPage,
    'workboard.workgroup.edit':WorkGroupFormPage,
    
    'workboard.worknode.edit':WorkNodeFormPage,
    
    'workboard.busclient':ClientPage,
    'workboard.busclient.edit':ClientFormPage,
})


