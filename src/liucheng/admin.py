# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,page_dc,ModelFields,FormPage,model_dc,regist_director,RowFilter,\
     RowSort,RowSearch,form_dict,permit_list,has_permit,PageNum
from .models import NodeGroup,WorkNode,BusClient
from helpers.director.db_tools import to_dict
import json
from .mobile_admin import *
from helpers.case.organize.models import Employee
from django.core.exceptions import PermissionDenied
from django import forms

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
            exclude=['kind']
        
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
    
    class NodeRecordNum(PageNum):
        perPage=10
    
    class NodeRecordFilter(RowFilter):
        model=NodeGroup
        names=['client','node_status','owner']   
        range_fields =[{'name':'start_time','type':'date'}]
        
        def get_context(self):
            ls=super(self.__class__,self).get_context()
            user_options=[]
            for emp in Employee.objects.all():
                user_options.append({'value':emp.pk,'label':unicode(emp)})
            ls.append({'name':'owner','label':'负责人','options':user_options})
            ls.append({'name':'start_time','type':'date','label':'节点启动时间'})
            option=[{'value':'waiting','label':'等待'},
                    {'value':'finish','label':'完成'}]
            ls.append({'name':'node_status','label':'包含节点状态','options':option})
            return ls
        
        def get_query(self,query):
            self.query=query
            owner=self.filter_args.pop('owner',None)

            start_time__gte=self.filter_args.pop('start_time__gte',None)
            start_time__lte=self.filter_args.pop('start_time__lte',None)
            node_status=self.filter_args.pop('node_status',None)
            
            if start_time__gte or start_time__lte or node_status or owner:
                node_filter_args={}
                if start_time__gte:
                    node_filter_args['start_time__gte']=start_time__gte
                if start_time__lte:
                    node_filter_args['start_time__lte']=start_time__lte
                if node_status:
                    node_filter_args['status']=node_status
                if owner:
                    node_filter_args['owner_id']=owner
                nodes_query=WorkNode.objects.filter(**node_filter_args)
                if start_time__gte or start_time__lte:  # 张容智商有问题，看来只能排除掉未设置时间项目的干扰，她才能理解
                                                        # 当过滤时间时，把未设置时间的项，排除开。
                    nodes_query=nodes_query.exclude(start_time='')

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
            else:
                return query      
        
    class NodeRecordTable(ModelTable):
        model=NodeGroup
        
        def inn_filter(self, query):
            query= query.filter(kind='workrecord').order_by('-id')
            if not self.permit.can_access():
                raise PermissionDenied,'没有权限访问工作流程图'
            if not has_permit(self.crt_user,'nodegroup.checkall'):
                emp=self.crt_user.employee_set.first()
                query = query.filter(worknode__owner=emp).distinct()
            return query
                
        
        def dict_row(self, inst):
            nodes=[]
            for node in inst.worknode_set.all():
                node_dc=to_dict(node) # form_dict(node,user=self.crt_user) # to_dict(node)  #
                if node.owner and node.owner.baseinfo:
                    node_dc['head_img']=node.owner.baseinfo.head
                nodes.append(node_dc)
                
            dc={
                'nodes': nodes , # [to_dict(x) for x in  inst.worknode_set.all()],
                'client':unicode(inst.client) if inst.client else ''
                #'relations':inst.relations
            }
            return dc   
    NodeRecordTable.pagenator=NodeRecordNum
    NodeRecordTable.filters=NodeRecordFilter
    NodeRecordTable.sort=WorkSort
    NodeRecordTable.search=NodeGroupSearch
    
    tableCls=NodeRecordTable
    def get_template(self, prefer=None):
        if prefer=='f7':
            return 'liucheng/liucheng_f7.html'
        else:
            return 'liucheng/liucheng.html'

 
class NodeGroupTemplatePage(TablePage):
    
    class NodeGroupTemplateTable(NodeRecordPage.NodeRecordTable):
        include=['id','short_desp','relations']
        def inn_filter(self, query):
            if not has_permit(self.crt_user,'nodegroup.edit_template'):
                raise PermissionDenied,'你没有权限编辑模板'
            return query.filter(kind='template')    
    
    NodeGroupTemplateTable.filters=RowFilter
    NodeGroupTemplateTable.search=RowSearch
    
    tableCls=NodeGroupTemplateTable
    template='liucheng/liucheng_template.html'
    
    

class WorkNodeFormPage(FormPage):
    
    class WorkNodeForm(ModelFields):
        def __init__(self,*args,**kw):
            super(self.__class__,self).__init__(*args,**kw)
            self.emp=self.crt_user.employee_set.first()
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
                
          # 不是当前员工的节点，不允许其编辑任何字段。
            if not has_permit(self.crt_user,'nodegroup.check_all') and self.instance.owner!=self.emp:
                head['readonly']=True
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


#class NodeGroupPageF7(TablePage):
    #class NodeGroupTable(ModelTable):
        #model=NodeGroup
        
        #def dict_row(self, inst):
            #dc={
                ##'nodes': [to_dict(x) for x in  inst.worknode_set.all()],
                #'client':unicode(inst.client) if inst.client else ''
            #}
            #return dc  
    #tableCls=NodeGroupTable



model_dc[WorkNode]={'fields':WorkNodeFormPage.WorkNodeForm}
model_dc[NodeGroup]={'fields':NodeRrecordFormPage.NodeRecordForm}

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

class ClientForm(ModelFields):
    class Meta:
        model=BusClient
        exclude=[]
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if BusClient.objects.filter(name=name):
            raise forms.ValidationError('公司名字重复')
        return name

regist_director(name='busclient',src_model=BusClient)
page_dc['busclient'].tableCls.sort=ClientSort
model_dc[BusClient]={'fields':ClientForm}

page_dc.update({
    'liucheng':NodeRecordPage,
    'liucheng.edit':NodeRrecordFormPage,
    'liucheng.f7': NodeRecordPage, #NodeGroupPageF7,
    'liucheng.f7.edit':NodeRrecordFormPage,
    
    'node.f7.edit':WorkNodeFormPage,
    
    'worknode':WorkNodeTablePage,
    'worknode.edit':WorkNodeFormPage,
    'nodegrouptemplate':NodeGroupTemplatePage,
    'nodegrouptemplate.edit':NodeRrecordFormPage,
})

permit_list.append(WorkNode)
permit_list.append(NodeGroup)
# permit_list.append(BusClient)
permit_list.append({'name':'nodegroup','label':'liucheng.nodegroup_SP','fields':[
    {'name':'check_all','label':'查看所有流程','type':'bool'},
    {'name':'edit_template','label':'编辑模板','type':'bool'},
]})