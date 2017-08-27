# encoding:utf-8
from __future__ import unicode_literals
from .models import NodeGroup,WorkNode
from helpers.director.db_tools import to_dict,from_dict

def get_global():
    return globals()

def add_new_record(row=None):
    obj = NodeGroup.objects.create(kind='workrecord')
    if row:
        src_nodegroup=from_dict(row)
        obj.copy(src_nodegroup)
    dc=to_dict(obj)
    dc['nodes']=[]
    return {'record':dc}

def create_node(node_group):
    node_group=from_dict(node_group)
    node = WorkNode.objects.create(node_group=node_group)
    return to_dict(node)

def save_node_group(node_group):
    node_group=from_dict(node_group)
    node_group.save()
    return {'status':'success'}

def add_node_template():
    obj = NodeGroup.objects.create(kind='template')
    dc=to_dict(obj)
    dc['nodes']=[]
    return {'record':dc}
