# encoding:utf-8


def get_empgroup(TabGroup,EmployeeItem,BaseinfoItem,BasicInfo,and_list,User,UserTab,Employee,evalue_container,**kw):
    
    class EmpGroup(TabGroup):
        tabs=[{'name':'emp','label':'员工','page_cls':EmployeeItem},
              {'name':'baseinfo','label':'基本信息','page_cls':BaseinfoItem,'visible':and_list([BasicInfo])},
              {'name':'user','label':'账号','page_cls':UserTab,'visible':and_list([User])},
              # {'name':'permit','label':'工作权限','page_cls':EmployePermitTab,'visible':and_list(
                  # [WorkPermitModel])}
              ]
        
        def get_tabs(self):
            emp_pk=self.request.GET.get('pk')
            tabs= self.tabs
            if not emp_pk:      # 没有emp_pk 表示是新建employee
                tabs= self.tabs[0:1]
            else:
                emp= Employee.objects.get(pk=emp_pk)
                if not emp.user:        # 没有账号时，不显示账号标签
                    tabs=[x for x in tabs if x['name']!='user']
                
            tabs= evalue_container(tabs,user=self.request.user)
            return tabs
    
    return EmpGroup

