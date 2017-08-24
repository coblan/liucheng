from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,page_dc,ModelFields,FormPage,model_dc,regist_director,RowFilter,RowSort
from .models import NodeGroup,WorkNode,BusClient
from helpers.director.db_tools import to_dict
import json

# Register your models here.
class NodeRecordForm(ModelFields):
    
    def get_row(self):
        """
        convert self.instance to dict.
        Note:Only convert Meta.fields ,not All fields
        """
        if not self.can_access():
            raise PermissionDenied,'you have no Permission access %s'%self.instance._meta.model_name
        dc=to_dict(self.instance)
        if self.instance.relations:
            relations=json.loads(self.instance.relations)
        else:
            relations=[]
        dc.update({
            'nodes': [to_dict(x) for x in  self.instance.worknode_set.all()],
            'relations':relations,
        })
        
        return dc
    
    class Meta:
        model=NodeGroup
        exclude=[]

class NodeRrecordFormPage(FormPage):
    fieldsCls=NodeRecordForm
    template='liucheng/liucheng_form.html'

class NodeRecordTable(ModelTable):
    model=NodeGroup
    
    def dict_row(self, inst):
        dc={
            'nodes': [to_dict(x) for x in  inst.worknode_set.all()]
        }
        return dc
    
class NodeRecordPage(TablePage):
    tableCls=NodeRecordTable
    template='liucheng/liucheng.html'

class WorkNodeFilter(RowFilter):
    model=WorkNode
    names=['status','client']
    
class WorkSort(RowSort):
    names=['mtime']

class WorkNodeForm(ModelFields):
    class Meta:
        model=WorkNode
        exclude=[]

class WorkNodeFormPage(FormPage):
    fieldsCls=WorkNodeForm

class WorkNodeTable(ModelTable):
    model=WorkNode
    filters=WorkNodeFilter
    sort=WorkSort
    
    def dict_row(self, inst):
        return {
            'client':unicode(inst.client) if inst.client else ''
        }

class WorkNodeTablePage(TablePage):
    tableCls=WorkNodeTable

model_dc[WorkNode]={'fields':WorkNodeForm}

regist_director(name='busclient',src_model=BusClient)

page_dc.update({
    'liucheng':NodeRecordPage,
    'liucheng.edit':NodeRrecordFormPage,
    'worknode':WorkNodeTablePage,
    'worknode.edit':WorkNodeFormPage,
})