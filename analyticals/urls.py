from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginView.as_view(), name='loginView'),
    path('stockPick', views.stockPickView.as_view(), name='stockPickView'),
    path('graphDisplay', views.graphDisplayView.as_view(), name='graphDisplayView'),
]
