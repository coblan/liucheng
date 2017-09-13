# encoding:utf-8
from __future__ import unicode_literals
from .models import NodeGroup,WorkNode
from helpers.director.db_tools import to_dict,from_dict
from .admin import NodeRrecordFormPage
from django.utils import timezone
from helpers.director.decorator import need_login


def get_global():
    return globals()

def add_new_record(request,row=None):
    obj = NodeGroup.objects.create(kind='workrecord')
    if row:
        src_nodegroup=from_dict(row)
        obj.copy(src_nodegroup)
    form = NodeRrecordFormPage.NodeRecordForm(instance=obj,crt_user=request.user)
    dc=form.get_row() # to_dict(obj)
    # dc['nodes']=[]
    return {'record':dc}

def create_node(node_group):
    node_group=from_dict(node_group)
    node = WorkNode.objects.create(node_group=node_group)
    return to_dict(node)

def save_node_group(node_group):
    nodes=node_group.get('nodes',[])
    nodes=[from_dict(x) for x in nodes]
    node_group=from_dict(node_group)
    for node in node_group.worknode_set.all():
        if node not in  nodes:
            node.delete()
    
    node_group.save()
    return {'status':'success'}

def add_node_template():
    obj = NodeGroup.objects.create(kind='template')
    dc=to_dict(obj)
    dc['nodes']=[]
    return {'record':dc}

# def delete_nodes(nodes):
    # for node_dc in nodes:
        # node=from_dict(node_dc)
        # node.delete()
    # return {'status':'success'}

def get_emp_node_info(user):
    emp=user.employee_set.first()
    now = timezone.now()
    now=timezone.localtime(now)
    today=now.strftime('%Y-%m-%d')
    today_query=WorkNode.objects.filter(owner=emp,start_time=today)
    today_count=today_query.count()
    today_finish_count=today_query.filter(status='finish').count()
    
    old_query = WorkNode.objects.filter(owner=emp,start_time__lt=today,status='waiting')
    old_count=old_query.count()
    
    this_month_start=today[:7]
    month_query = WorkNode.objects.filter(owner=emp,start_time__startswith=this_month_start,status='finish')
    month_count=month_query.count()
    return {
        'employee':user.first_name,
        'today_count':today_count,
        'today_finish_count':today_finish_count,
        'old_waiting_count':old_count,
        'month_finish_count':month_count,
    }


def get_node_info():
    now = timezone.now()
    now=timezone.localtime(now)
    today=now.strftime('%Y-%m-%d')
    today_query=WorkNode.objects.filter(start_time=today)
    today_count=today_query.count()
    today_finish_count=today_query.filter(status='finish').count()
    
    old_query = WorkNode.objects.filter(start_time__lt=today,status='waiting',start_time__isnull=False)
    old_count=old_query.count()
    
    this_month_start=today[:7]
    month_query = WorkNode.objects.filter(start_time__startswith=this_month_start,status='finish')
    month_count=month_query.count()
    return {
        'today_count':today_count,
        'today_finish_count':today_finish_count,
        'old_waiting_count':old_count,
        'month_finish_count':month_count,
    }    