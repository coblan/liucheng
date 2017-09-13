from helpers.case.site_frame.admin import F7HomeWraper
from helpers.director.shortcut import page_dc

class MyF7Home(F7HomeWraper):
    need_login=True

page_dc.update({
    'home.f7':MyF7Home
})