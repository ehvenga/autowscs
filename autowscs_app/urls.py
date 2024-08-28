from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('add_webservice', add_webservice, name='add_webservice'),
    path('delete_webservice', delete_webservice, name='delete_webservice'),
    path('add_parameter', add_parameter, name='add_parameter'),
    path('delete_parameter', delete_parameter, name='delete_parameter'),
    path('add_inputparameter', add_inputparameter, name='add_inputparameter'),
    path('delete_inputparameter', delete_inputparameter, name='delete_inputparameter'),
    path('add_parameterhierarchy', parameterhierarchy, name='add_parameterhierarchy'),
    path('parameterhierarchy', parameterhierarchy_data, name='parameterhierarchy_data'),
    path('org_chart', org_chart, name='org_chart'),
    path('upload_datafile', upload_datafile, name='upload_datafile'),
    path('show', show, name="show"),
    path('show_result', show_result, name="show_result"),
    #path('show_result_temp', show_result_temp, name="show_result_temp"),
    path('show_result_static', show_result_static, name="show_result_static"),


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)