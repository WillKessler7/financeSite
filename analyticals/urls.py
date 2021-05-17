from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginView.as_view(), name='loginView'),
    path('stockPick', views.stockPickView.as_view(), name='stockPickView'),
    path('stockDisplay', views.stockDisplayView.as_view(), name='stockDisplayView'),
    path('loginView', views.loginView.as_view(), name='loginView'),
]
