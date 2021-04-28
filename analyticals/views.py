from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.template import loader
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Stock, PortEntries

class loginView(View):
    def post(self, request):


        # if the username imported from template's form is for logging in,
        if 'inputedUsername' in request.POST.keys():

            # try to authenticate the inputed username and password
            user = authenticate(username=request.POST['inputedUsername'],\
            password=request.POST['inputedPassword'])

        # if the user was found (authenticated),
        if user is not None:
            # login the user
            login(request, user)

        # otherwise, if the user was not found,
        else:
            # failed login
            pass
        #else:
            #logout(request)

        # the following two lines are for testing user authentication
        password = request.POST['inputedPassword']
        return HttpResponse(password)

    def get(self, request):

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
