# encoding:utf-8

from helpers.director.shortcut import TablePage,ModelTable,page_dc,ModelFields,FormPage,model_dc,regist_director,RowFilter,RowSort,RowSearch
from .models import NodeGroup


class NodeGroupPage(TablePage):
    class NodeGroupTable(ModelTable):
        model=NodeGroup
        
        def dict_row(self, inst):
            dc={
                #'nodes': [to_dict(x) for x in  inst.worknode_set.all()],
                'client':unicode(inst.client) if inst.client else ''
            }
            return dc        


page_dc.update({
    'liucheng.f7':NodeGroupPage,
    #'liucheng.f7.edit':
})