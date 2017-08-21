# encoding=utf-8

from django.contrib.auth.models import User,Group
from helpers.director.engine import BaseEngine,page,can_touch,can_list,fa
from helpers.case.organize import menu as organize_menu
from helpers.director.shortcut import page_dc
from helpers.director.models import KVModel
from helpers.pageadaptor.models import WebPage

class PcMenu(BaseEngine):
    url_name='liucheng'
    menu=[
        {'label':'home','url':page('press',append='?_name=home'),'icon':fa('fa-home')},
        {'label':'账号管理','url':page('user'),'icon':fa('fa-users'),'visible':can_list((User,Group)),
         'submenu':[
                    {'label':'用户管理','url':page('user'),'visible':can_touch(User)},
                    {'label':'用户组','url':page('group'),'visible':can_touch(Group)},
                    ]},

        organize_menu.pc_menu,
        
        {'label':'Page Admin','url':page('webpage'),'icon':fa('fa-home'),'visible':can_touch(WebPage)},
        {'label':'设置','url':page('kv'),'icon':fa('fa-home'),'visible':can_touch(KVModel)},
    ]        
    

class MbMenu(BaseEngine):
    url_name='liucheng_mobile'
    

PcMenu.add_pages(page_dc)
MbMenu.add_pages(page_dc)