from .models import WorkNode
from django.utils import timezone
from helpers.director.db_tools import from_dict,to_dict,permit_to_dict

def get_global():
    return globals()


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

#def create_worknode_from_temp(temp,user):
    #temp_obj=from_dict(temp)
    #node = temp_obj.create_node()
    #dc=  permit_to_dict(user,node)
    #dc["nodes"]=[permit_to_dict(user,x) for x in  node.worknode_set.order_by('id')]
    #return dc
