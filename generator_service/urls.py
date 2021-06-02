"""generation_system URL Configuration

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
from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('',views.redirect_views,name="redirect_views"),
    path('data-schemas',views.data_schemas_views,name="data_schemas_views"),
    path('new-schema',views.new_schema_views,name="new_schema_views"),
    path('edit-schema/<int:id>/',views.edit_schema_views,name="edit_schema_views"),
    path('add-schema',views.adding_new_schema_views,name="adding_new_schema_views"),
    path('update-schema/<int:id>',views.updating_schema_views,name="updating_schema_views"),
    path('data-sets/<int:id>',views.data_sets_views,name="data_sets_views"),
    path('generate/<int:id>/',views.generate_data_views,name="generate_data")
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)