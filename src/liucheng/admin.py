# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,page_dc,ModelFields,FormPage,model_dc,regist_director,RowFilter,RowSort,RowSearch
from .models import NodeGroup,WorkNode,BusClient
from helpers.director.db_tools import to_dict
import json
from .mobile_admin import *
from helpers.case.organize.models import Employee

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
            nodes=[]
            for node in self.instance.worknode_set.all():
                node_dc=to_dict(node)
                if node.owner and node.owner.baseinfo:
                    node_dc['head_img']=node.owner.baseinfo.head
                nodes.append(node_dc)
            dc.update({
                'nodes': nodes #[to_dict(x) for x in  self.instance.worknode_set.all()],
            })
            
            return dc
        
        class Meta:
            model=NodeGroup
            exclude=['relations','kind']
        
        def dict_head(self, head):
            if head['name']=='start_time':
                head['type']='date'
            return head
    
    fieldsCls=NodeRecordForm
    def get_template(self, prefer=None):
        if prefer=='f7':
            return 'liucheng/liucheng_form_f7.html'
        else:
            return 'liucheng/liucheng_form.html'


class NodeRecordPage(TablePage):
    
    class NodeRecordFilter(RowFilter):
        model=NodeGroup
        names=['client','node_status']   
        range_fields =[{'name':'start_time','type':'date'}]
        
        def get_context(self):
            ls=super(self.__class__,self).get_context()
            ls.append({'name':'start_time','type':'date','label':'节点指派时间'})
            
            option=[{'value':'waiting','label':'等待'},
                    {'value':'finish','label':'完成'}]
            ls.append({'name':'node_status','label':'包含节点状态','options':option})
            return ls
        
        def get_query(self,query):
            self.query=query
            start_time__gte=self.filter_args.pop('start_time__gte',None)
            start_time__lte=self.filter_args.pop('start_time__lte',None)
            node_status=self.filter_args.pop('node_status',None)
            
            if start_time__gte or start_time__lte or node_status:
                node_filter_args={}
                if start_time__gte:
                    node_filter_args['start_time__gte']=start_time__gte
                if start_time__lte:
                    node_filter_args['start_time__lte']=start_time__lte
                if node_status:
                    node_filter_args['status']=node_status
                nodes_query=WorkNode.objects.filter(**node_filter_args)
                # record_pk_list=[]
                # for node in nodes_query:
                    # record_pk_list.append(node.node_group.pk)
                # record_pk_list=list(set(record_pk_list))
                # query=query.filter(pk__in=record_pk_list)
                query=query.filter(worknode__in=nodes_query).distinct()
                
            query=query.filter(**self.filter_args)
            return query  
        
    
    class WorkSort(RowSort):
        names=['start_time']
    
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
            return query.filter(kind='workrecord').order_by('-id')
        
        def dict_row(self, inst):
            nodes=[]
            for node in inst.worknode_set.all():
                node_dc=to_dict(node)
                if node.owner and node.owner.baseinfo:
                    node_dc['head_img']=node.owner.baseinfo.head
                nodes.append(node_dc)
                
            dc={
                'nodes': nodes , # [to_dict(x) for x in  inst.worknode_set.all()],
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
    
    NodeGroupTemplateTable.filters=RowFilter
    NodeGroupTemplateTable.search=RowSearch
    
    tableCls=NodeGroupTemplateTable
    template='liucheng/liucheng_template.html'
    
    

class WorkNodeFormPage(FormPage):
    
    class WorkNodeForm(ModelFields):
        class Meta:
            model=WorkNode
            exclude=['node_group']
        
        def get_row(self):
            row=super(self.__class__,self).get_row()
            node=self.instance
            if node.owner and node.owner.baseinfo:
                row['head_img']=node.owner.baseinfo.head     
            return row
        
        def dict_head(self, head):
            if head['name']=='start_time':
                head['type']='date'
            return head
        
    fieldsCls=WorkNodeForm
    
    def get_template(self, prefer=None):
        if prefer=='f7':
            return 'liucheng/node_form_f7.html'
        else:
            return 'director/fields.html'


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


class NodeGroupPageF7(TablePage):
    class NodeGroupTable(ModelTable):
        model=NodeGroup
        
        def dict_row(self, inst):
            dc={
                #'nodes': [to_dict(x) for x in  inst.worknode_set.all()],
                'client':unicode(inst.client) if inst.client else ''
            }
            return dc  
    tableCls=NodeGroupTable


model_dc[WorkNode]={'fields':WorkNodeFormPage.WorkNodeForm}
model_dc[NodeGroup]={'fields':NodeRrecordFormPage.NodeRecordForm}
regist_director(name='busclient',src_model=BusClient)

page_dc.update({
    'liucheng':NodeRecordPage,
    'liucheng.edit':NodeRrecordFormPage,
    'liucheng.f7':NodeGroupPageF7,
    'liucheng.f7.edit':NodeRrecordFormPage,
    
    'node.f7.edit':WorkNodeFormPage,
    
    'worknode':WorkNodeTablePage,
    'worknode.edit':WorkNodeFormPage,
    'nodegrouptemplate':NodeGroupTemplatePage,
    'nodegrouptemplate.edit':NodeRrecordFormPage,
})