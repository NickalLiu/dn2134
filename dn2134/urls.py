from django.conf.urls import include, url
from django.contrib import admin
from main.views import exam, wechat_main


urlpatterns = [
    # Examples:
    # url(r'^$', 'dn2134.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^exam/', exam),
	url(r'^wechat/', wechat_main),
]
