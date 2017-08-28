# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,page_dc,ModelFields,FormPage,model_dc,regist_director,RowFilter,RowSort,RowSearch
from .models import NodeGroup,WorkNode,BusClient
from helpers.director.db_tools import to_dict
import json

# Register your models here.

class NodeRrecordFormPage(FormPage):
    
    class NodeRecordForm(ModelFields):
        
        def get_row(self):
            """
            convert self.instance to dict.
            Note:Only convert Meta.fields ,not All fields
            """
            if not self.can_access():
                raise PermissionDenied,'you have no Permission access %s'%self.instance._meta.model_name
            dc=to_dict(self.instance)
            #if self.instance.relations:
                #relations=json.loads(self.instance.relations)
            #else:
                #relations=[]
            dc.update({
                'nodes': [to_dict(x) for x in  self.instance.worknode_set.all()],
            })
            
            return dc
        
        class Meta:
            model=NodeGroup
            exclude=['relations']    
    
    fieldsCls=NodeRecordForm
    template='liucheng/liucheng_form.html'


class NodeRecordPage(TablePage):
    
    class NodeRecordFilter(RowFilter):
        model=NodeGroup
        names=['client']    
    
    class WorkSort(RowSort):
        names=['create_time']
    
    class NodeGroupSearch(RowSearch):
        model=NodeGroup
        def get_context(self):
            return '简约说明'
    
        def get_query(self,query):
            if self.q:
                exp=None
                return query.filter(short_desp__icontains=self.q)
                #for name in self.valid_name:
                    #kw ={}
                    #kw['%s__icontains'%name] =self.q    
                    #if exp is None:
                        #exp = Q(**kw)
                    #else:
                        #exp = exp | Q(**kw) 
                #return query.filter(exp)
            else:
                return query      
        
    class NodeRecordTable(ModelTable):
        model=NodeGroup
        
        def inn_filter(self, query):
            return query.filter(kind='workrecord')
        
        def dict_row(self, inst):
            #if inst.relations:
                #relations=json.loads(inst.relations)
            #else:
                #relations=[]
            dc={
                'nodes': [to_dict(x) for x in  inst.worknode_set.all()],
                'client':unicode(inst.client) if inst.client else ''
                #'relations':inst.relations
            }
            return dc    
    NodeRecordTable.filters=NodeRecordFilter
    NodeRecordTable.sort=WorkSort
    NodeRecordTable.search=NodeGroupSearch
    
    tableCls=NodeRecordTable
    template='liucheng/liucheng.html'

 
class NodeGroupTemplatePage(TablePage):
    
    class NodeGroupTemplateTable(NodeRecordPage.NodeRecordTable):
        include=['id','short_desp','relations']
        def inn_filter(self, query):
            return query.filter(kind='template')    
        
    tableCls=NodeGroupTemplateTable
    template='liucheng/liucheng_template.html'
    
    

class WorkNodeFormPage(FormPage):
    
    class WorkNodeForm(ModelFields):
        class Meta:
            model=WorkNode
            exclude=[]
        
    fieldsCls=WorkNodeForm


class WorkNodeTablePage(TablePage):
    
    class WorkNodeFilter(RowFilter):
        model=WorkNode
        names=['status','client']
        
    class WorkSort(RowSort):
        names=['mtime']
    
    class WorkNodeTable(ModelTable):
        model=WorkNode

        # def dict_row(self, inst):
            # return {
                # 'client':unicode(inst.client) if inst.client else ''
            # }
    WorkNodeTable.filters=WorkNodeFilter
    WorkNodeTable.sort=WorkSort
    
    tableCls=WorkNodeTable


model_dc[WorkNode]={'fields':WorkNodeFormPage.WorkNodeForm}

regist_director(name='busclient',src_model=BusClient)

page_dc.update({
    'liucheng':NodeRecordPage,
    'liucheng.edit':NodeRrecordFormPage,
    'worknode':WorkNodeTablePage,
    'worknode.edit':WorkNodeFormPage,
    'nodegrouptemplate':NodeGroupTemplatePage,
    'nodegrouptemplate.edit':NodeRrecordFormPage,
})