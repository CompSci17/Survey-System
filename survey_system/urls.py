from django.conf.urls import patterns, include, url
from django.contrib import admin

from survey_system_files.views import survey_list, survey_detail, survey_results

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'survey_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', survey_list, name = "survey_list"),
    url(r'^survey/(?P<pk>\d+)/$', survey_detail, name = "survey_detail"),
    url(r'^survey/(?P<pk>\d+)/results/$', survey_results, name = "survey_results"),

    url(r'^admin/', include(admin.site.urls)),

)
