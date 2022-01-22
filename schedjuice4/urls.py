"""schedjuice4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("reminder.urls")),
    path("api/v1/", include("staff_stuff.urls")),
    path("api/v1/", include("work_stuff.urls")),
    path("api/v1/", include("role_stuff.urls")),
    path("api/v1/", include("ms_stuff.urls")),
    path("api/v1/", include("wiki.urls")),
    path("api/v1/", include("student_stuff.urls"))
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass
