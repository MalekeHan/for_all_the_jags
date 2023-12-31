"""
URL configuration for spot_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

#from spot.views import SearchView
from spot.views import SearchViewSet, SurveyViewSet, SurveyAggregateView

"""
from views import viewsets
"""

router = DefaultRouter()
"""
register routes here
router.register(r'ROUTE', VIEWSET)
"""
router.register(r'search', SearchViewSet, basename='search')
router.register(r'surveys', SurveyViewSet)

urlpatterns = [
    path('', include(router.urls)),
   # path('search/', SearchView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('aggregate/', SurveyAggregateView.as_view(), name='survey-aggregate'),
]
