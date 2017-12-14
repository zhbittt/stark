from django.conf.urls import url
from django.shortcuts import render,HttpResponse
from django.conf.urls.i18n import i18n_patterns
class StarkConfig(object):
    list_display=[]




    def __init__(self,model_class,site):
        self.model_class=model_class
        self.site=site

    @property
    def urls(self):
        return self.get_urls()


    def get_urls(self):
        app_model_name=(self.model_class._meta.app_label,self.model_class._meta.model_name,)
        url_patterns = [
            url(r'^$',self.changelist_view,name="%s_%s_changelist"%app_model_name),
            url(r'^add/$',self.add_view,name="%s_%s_add"%app_model_name),
            url(r'^(\d+)/delete/$',self.delete_view,name="%s_%s_delete"%app_model_name),
            url(r'^(\d+)/change/$',self.change_view,name="%s_%s_change"%app_model_name),
        ]
        return url_patterns


    def inner_table_body(self, data_list):
        new_data_list = []
        for row in data_list:
            temp = []
            for field_name in self.list_display:
                if isinstance(field_name, str):
                    val = getattr(row, field_name)
                else:
                    val = field_name(self, row)
                temp.append(val)
            new_data_list.append(temp)
        yield from new_data_list

    def inner_table_head(self):
        head_list = []
        if not self.list_display:
            obj_list = self.model_class.objects.all()
            for i in obj_list:
                head_list.append(i)
        else:
            for field_name in self.list_display:
                if isinstance(field_name, str):
                    verbose_name = self.model_class._meta.get_field(field_name).verbose_name
                else:
                    verbose_name = field_name(self, is_header=True)
                head_list.append(verbose_name)
        yield from head_list


    def changelist_view(self,request,*args,**kwargs):
        #处理表头
        # head_list=[]
        #
        # if not self.list_display:
        #     obj_list=self.model_class.objects.all()
        #     for i in obj_list:
        #         head_list.append(i)
        # else:
        #     for field_name in self.list_display:
        #         if isinstance(field_name,str):
        #             verbose_name=self.model_class._meta.get_field(field_name).verbose_name
        #         else:
        #             verbose_name=field_name(self,is_header=True)
        #         head_list.append(verbose_name)


        #处理表内数据
        data_list=self.model_class.objects.all()


        # new_data_list=[]
        # for row in data_list:
        #     temp=[]
        #     for field_name in self.list_display:
        #         if isinstance(field_name,str):
        #             val=getattr(row,field_name)
        #         else:
        #             val=field_name(self,row)
        #         temp.append(val)
        #
        #     new_data_list.append(temp)

        # request.session["table_head"]=head_list
        # request.session["table_body"]=new_data_list






        return render(request,"stark/changelist.html",{"data_list":self.inner_table_body(data_list),"head_list":self.inner_table_head()})


    def add_view(self,request,*args,**kwargs):
        return HttpResponse("添加")

    def delete_view(self,request,nid,*args,**kwargs):
        return HttpResponse("删除")

    def change_view(self,request,nid,*args,**kwargs):
        return HttpResponse("修改")



class StrakSite(object):
    def __init__(self):
        self._registry={}

    def register(self,model_class,stark_config_class=None):
        if not stark_config_class:
            stark_config_class=StarkConfig
        self._registry[model_class]=stark_config_class(model_class,self)


    @property
    def urls(self):
        return self.get_urls(),None,"stark"

    def get_urls(self):
        url_patterns=[]

        for model_class,stark_config_obj in self._registry.items():

            app_name=model_class._meta.app_label
            model_name=model_class._meta.model_name

            curd_url=url(r'^%s/%s/'%(app_name,model_name),(stark_config_obj.urls,None,None))

            url_patterns.append(curd_url)

        return url_patterns

site=StrakSite()
