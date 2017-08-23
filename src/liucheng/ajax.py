# encoding:utf-8
from __future__ import unicode_literals
from .models import NodeGroup,WorkNode
from helpers.director.db_tools import to_dict,from_dict

def get_global():
    return globals()

def add_new_record():
    obj = NodeGroup.objects.create()
    return {'record':to_dict(obj)}

def create_node(node_group):
    node_group=from_dict(node_group)
    node = WorkNode.objects.create(node_group=node_group)
    return to_dict(node)

def  save_node_group(node_group):
    pass
