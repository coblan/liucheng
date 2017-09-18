# encoding:utf-8

from django.contrib import admin
from helpers.director.shortcut import ModelTable,TablePage,page_dc,FormPage,ModelFields,model_dc,RowSort,RowFilter,RowSearch
from helpers.director.db_tools import permit_to_dict
from .models import WorkGroup,BusClient,WorkNode
from helpers.case.organize.models import Employee
# Register your models here.
class WorkGroupPage(TablePage):
    template='workboard/workboard.html'
    
    class WorkGroupFilter(RowFilter):
        names=['client','node_status','owner']
        range_fields=[{'name':'start_time','type':'date'}]
        
        def get_context(self):
            ls=super(self.__class__,self).get_context()
            for f in ls:
                if f['name']=='client':
                    f['type']='sel-search-filter'
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
    
    class NodeGroupSearch(RowSearch):
        model=WorkGroup
        def get_context(self):
            return '简约说明'
    
        def get_query(self,query):
            if self.q:
                exp=None
                return query.filter(short_desp__icontains=self.q)
            else:
                return query 
            
    class WorkGroupTable(ModelTable):
        model=WorkGroup
        exclude=[]
        
        def dict_row(self, inst):

            return {
                "client":unicode(inst.client) if inst.client else "",
                "nodes":[permit_to_dict(self.crt_user,x) for x in  inst.worknode_set.order_by('id')]
                }
    WorkGroupTable.filters=WorkGroupFilter
    WorkGroupTable.search=NodeGroupSearch
    
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
        def dict_head(self, head):
            if head['name']=='client':
                head['type']='search_select'
            return head
        
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


