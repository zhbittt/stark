
from django.template import Library
from django.conf import settings
import re
register = Library()
@register.inclusion_tag("xxxxx.html")
def table_html(request):

    table_dict={}
    table_body_data=request.session.get("data_list")
    table_head_data=request.session.get("head_list")

    table_dict["table_body_data"]=table_body_data
    table_dict["table_head_data"]=table_head_data

    return {'table_dict':table_dict}