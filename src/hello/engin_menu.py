# encoding=utf-8

from django.contrib.auth.models import User,Group
from helpers.director.engine import BaseEngine,page,can_touch,can_list,fa
from helpers.case.organize import menu as organize_menu
from helpers.director.shortcut import page_dc,has_permit
from helpers.director.models import KVModel
from helpers.pageadaptor.models import WebPage
from helpers.maintenance.update_static_timestamp import js_stamp
from liucheng.models import BusClient,NodeGroup

class PcMenu(BaseEngine):
    url_name='liucheng'
    menu=[
        {'label':'home','url':page('press',append='?_name=home'),'icon':fa('fa-home')},
        {'label':'账号与权限','url':page('user'),'icon':fa('fa-users'),'visible':can_list((User,Group)),
         'submenu':[
                    {'label':'账号管理','url':page('user'),'visible':can_touch(User)},
                    {'label':'权限组','url':page('group'),'visible':can_touch(Group)},
                    ]},

        organize_menu.pc_menu,
        
        {'label':'工作流程','url':page('liucheng'),'icon':fa('fa-eye'),'visible':can_touch(NodeGroup),
         'submenu':[
             {'label':'工作流程','url':page('liucheng'),'visible':can_touch(NodeGroup)},
             {'label':'流程模板','url':page('nodegrouptemplate'),'visible':lambda user:has_permit(user,'nodegroup.edit_template')},
             
             # {'label':'工作列表','url':page('worknode'),},
             {'label':'客户信息','url':page('busclient'),'visible':can_touch(BusClient)},
             
             ]},
        
        {'label':'通用页面','url':page('webpage'),'icon':fa('fa-file-code-o'),'visible':can_touch(WebPage)},
        {'label':'系统设置','url':page('kv'),'icon':fa('fa-cog'),'visible':can_touch(KVModel)},
    ]      
    
    def custome_ctx(self, ctx):
        ctx['js_stamp']=js_stamp
        # engine_press=Press(help_name)
        # if engine_press.page:
            # ctx['help_url']=self.get_url('press')+'?_name=%s'%help_name
        return ctx       
    

class F7Engine(BaseEngine):
    url_name='liucheng_mobile'
    prefer='f7'
    root_page='/f7/home.f7'
    
    menu=[
        {'name':'liucheng','label':'工作流程','url':page('liucheng.f7',append=lambda user:'?node_status=waiting&owner=%s'%user.employee_set.first().pk),'icon':fa('fa-map fa-2x')}
    ]
    
    def custome_ctx(self, ctx):
        ctx['js_stamp']=js_stamp
        return ctx       
    
    
    

PcMenu.add_pages(page_dc)
F7Engine.add_pages(page_dc)