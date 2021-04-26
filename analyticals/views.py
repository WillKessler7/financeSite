from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.template import loader
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Stock, PortEntries

class loginView(View):
    def get(self, request):
        # checks if data is present in the login form within the view
        if request.POST:
            pass
        template = loader.get_template('analyticals/loginView.html')
        context = {}
        return HttpResponse(template.render(context, request))

class stockPickView(View):
    def get(self, request):
        template = loader.get_template('analyticals/stockPickView.html')
        allStocks = Stock.objects.all()
        context = {'allStocks': allStocks }
        print(request.POST)
        return HttpResponse(template.render(context, request))

class graphDisplayView(View):
    def get(self, request):
        template = loader.get_template('analyticals/graphDisplayView.html')
        # put data in context for each view
        context = {}
        return HttpResponse(template.render(context, request))
