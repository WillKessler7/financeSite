from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginView.as_view(), name='loginView'),
    path('stockPick', views.stockPickView.as_view(), name='stockPickView'),
    path('stockDisplay', views.stockDisplayView.as_view(), name='stockDisplayView'),
    path('loginView', views.loginView.as_view(), name='loginView'),

    # this is for the stock loading template, and the url error template,
    # all of the data is processed in stock pick view
    path('stockLoadView', views.stockPickView.as_view(), name='stockLoadView'),
    path('urlErrorView', views.stockPickView.as_view(), name='stockLoadView'),
]
