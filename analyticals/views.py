from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .models import Stock, PortEntries
import yfinance as yf

class loginView(View):
    def post(self, request):
        # sets loggedIn var to False as default because user begins not
        # logged in
        loggedIn = False

        newUser = ""

        # try to authenticate the inputed username and password
        username = request.POST['inputedUsername']
        password = request.POST['inputedPassword']


        # if the username imported from template's form is for logging in,
        if 'submit' in request.POST.keys():
            if request.POST['submit'] == 'login':

                user = authenticate(username=username, password=password)

                # if the user was found,
                if user is not None:
                    # login the user
                    login(request, user)
                    # set loggedIn var to true
                    loggedIn = True
                    # assign template to be loaded to the correct view
                    template = loader.get_template('analyticals/stockPickView.html')




                # otherwise, if the user was not found,
                else:
                    # loads back to the loginView template
                    template = loader.get_template('analyticals/loginView.html')

            # if the form submitted is not for logging in must be for creating acct
            elif request.POST['submit'] == 'create':
                template = loader.get_template('analyticals/stockPickView.html')
                newUser = User(username = request.POST['inputedUsername'],\
                password = make_password(request.POST['inputedPassword']))
                newUser.save()

        # otherwise, if a sumbit button was not found,
        else:
            # display to screen that submit was not found
            return HttpResponse("submit doesnt show")

        # save the variables of whether the user is loggedin and the username
        # to the correct template
        context = {
            'loggedIn': loggedIn,
            'username': username,
            'newUser': newUser,
        }

        return HttpResponse(template.render(context, request))


    def get(self, request):

        template = loader.get_template('analyticals/loginView.html')
        context = {}
        return HttpResponse(template.render(context, request))

class stockPickView(View):
    def post(self, request):
        """ program will iterate through the QQQ stock index and will show the
        stock ticker and company name to the user and the user can select if
        they want to follow the stock and view its information """

        # QQQ stock Index stocks that have full data with API
        stockIndex = ["THO", "MSFT", "AAPL", "AMZN", "FB", "GOOGL", "GOOG", "NFLX",\
        "NVDA", "PEP", "ADBE", "CSCO", "PYPL", "TSLA", "AMGN", "COST",\
        "AVGO", "TXN", "GILD", "QCOM", "SBUX", "TMUS", "INTU", "FISV",\
        "ADP", "AMD", "REGN", "BKNG", "ATVI", "BIIB", "CSX",\
        "ILMN", "JD", "ADSK", "ADI", "MELI", "WBA", "KHC", "LRCX", "EXC",\
        "EA", "EBAY", "ROST", "CTSH", "ORLY", "SGEN", "NXPI",\
        "BIDU", "MAR", "KLAC", "WDAY", "VRSK", "SIRI", "NTES", "VRSN",\
        "CSGP", "PCAR", "SNPS", "ANSS", "CDNS", "SPLK", "CTAS", "FAST",\
        "XLNX", "INCY", "CERN", "MCHP", "CPRT", "CTXS", "SWKS", "DLTR", "BMRN", \
        "ZM", "CHKP", "CDW", "TTWO", "MXIM", "ULTA", "WDC", "NTAP", "FOXA"]

        stockQuote = yf.Ticker(symbol)

        # stock ticker
        stock.ticker = stockQuote.info["symbol"]

        # name of the company
        stock.companyName = str(stockQuote.info["shortName"])

        # stock price
        stock.stockPrice = float(stockQuote.info["regularMarketOpen"])
        # fifty two week high
        stock.ftwh = float(stockQuote.info["fiftyTwoWeekHigh"])
        # fifty two week low
        stock.ftwl = float(stockQuote.info["fiftyTwoWeekLow"])

        # date stock was added
        stock.dateAdded = datetime.timezone.now()



        # checks if the form submission was for logging out
        if 'logoutButton' in request.POST.keys():
            # redirect to login view
            return redirect("loginView")

        else:
            template = loader.get_template('analyticals/stockDisplayView.html')
            context = {}
            return HttpResponse(template.render(context, request))

    def get(self, request):
        template = loader.get_template('analyticals/stockPickView.html')
        allStocks = Stock.objects.all()
        context = {'allStocks': allStocks }
        print(request.POST)
        return HttpResponse(template.render(context, request))

class stockDisplayView(View):
    def post(self, request):
            # checks if the form submission was for logging out
            if 'logoutButton' in request.POST.keys():
                # redirect to login view
                return redirect("loginView")

            else:
                # will work on the other case later
                template = loader.get_template('analyticals/stockDisplayView.html')
                context = {}
                return HttpResponse(template.render(context, request))

    def get(self, request):
        template = loader.get_template('analyticals/stockDisplayView.html')
        # put data in context for each view
        context = {}
        return HttpResponse(template.render(context, request))
