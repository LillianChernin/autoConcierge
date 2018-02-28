"""autoConcierge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include, handler404, handler500
from main_app import views as views
from main_app.views import index
# from main_app.views import index, SignUpView

urlpatterns = [
	url(r'admin/', admin.site.urls),
	url(r'', include('main_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/signup/', SignUpView.as_view(), name='signup'),
]

handler404 = views.error_404
handler500 = views.error_500