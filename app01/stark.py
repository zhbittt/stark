from stark.service import v1
from django.utils.safestring import mark_safe
from app01 import models

class UserInfoConfig(v1.StarkConfig):

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return "选择"
        return mark_safe("<input type='checkbox' name='pk' values='%s'>"%(obj.id))

    def edit(self,obj=None,is_header=False):
        if is_header:
            return "操作"

        return mark_safe("<a href='http://www.baidu.com'>编辑</a>")



    list_display = [checkbox,"id","name",edit]



v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.UserType)