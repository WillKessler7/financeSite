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

        # defines newUser as an empty string to initialize var
        newUser = ""

        username = request.POST['inputedUsername']
        password = request.POST['inputedPassword']


        # if the username imported from template's form is for logging in,
        if 'login' in request.POST.keys():

            # try to authenticate the inputed username and password
            user = authenticate(username=username, password=password)

            # if the user was found,
            if user is not None:
                # login the user
                login(request, user)
                # set loggedIn var to true
                loggedIn = True
                # assign template to be loaded to the correct view
                template = loader.get_template('analyticals/stockLoadView.html')




            # otherwise, if the user was not found,
            else:
                # loads back to the loginView template
                template = loader.get_template('analyticals/loginView.html')

        # if the form submitted is not for logging in must be for creating acct
        elif 'create' in request.POST.keys():
                template = loader.get_template('analyticals/stockPickView.html')
                newUser = User(username = request.POST['inputedUsername'],\
                password = make_password(request.POST['inputedPassword']))
                newUser.save()

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


        # because the user doesn't submit anything else when they log out, it
        # makes sense in terms of efficiency to check if the user logged out first
        # instead of loading data which the user won't use
        # checks if the form submission was for logging out
        if 'logoutButton' in request.POST.keys():
            # redirect to login view
            return redirect("loginView")

        # here is a list of the number of shares the user has for each stock
        shares = []

        # list of tickers of stocks that user owns
        userStocks = []

        # initializes variable used later for tracking number of user shares
        numShares = 0

        # this var indicates if the user has failed to correctly enter a ticker
        input = True

        # initializes a variable used in a for loop later
        stockQuote = ""

        symbols = request.POST.keys()
        print(symbols)

        """ program will iterate through the QQQ stock index and will show the
        stock ticker and company name to the user and the user can select if
        they want to follow the stock and view its information """

        # QQQ stock Index stocks that have full data with API
        stockIndex = ["THO", "MSFT"]
        """"MSFT", "AAPL", "AMZN", "FB", "GOOGL", "GOOG", "NFLX",\
        "NVDA", "PEP"]"""


        """, "ADBE", "CSCO", "PYPL", "TSLA", "AMGN", "COST",\
        "AVGO", "TXN", "GILD", "QCOM", "SBUX", "TMUS", "INTU", "FISV",\
        "ADP", "AMD", "REGN", "BKNG", "ATVI", "BIIB", "CSX"]"""


        """\
        "ILMN", "JD", "ADSK", "ADI", "MELI", "WBA", "KHC", "LRCX", "EXC",\
        "EA", "EBAY", "ROST", "CTSH", "ORLY", "SGEN", "NXPI",\
        "BIDU", "MAR", "KLAC", "WDAY", "VRSK", "SIRI", "NTES", "VRSN",\
        "CSGP", "PCAR", "SNPS", "ANSS", "CDNS", "SPLK", "CTAS", "FAST",\
        "XLNX", "INCY", "CERN", "MCHP", "CPRT", "CTXS", "SWKS", "DLTR", "BMRN", \
        "ZM", "CHKP", "CDW", "TTWO", "MXIM", "ULTA", "WDC", "NTAP", "FOXA"]"""


        # if the button clicked was to load the data,
        if 'load' in request.POST.keys():
            # load the same template
            template = loader.get_template('analyticals/stockPickView.html')

        # if the button was to save the user's data,
        elif 'addStock' in request.POST.keys() or 'turnIn' in request.POST.keys():
            # load the same template
            template = loader.get_template('analyticals/stockPickView.html')

            # if the inputed ticker matches one of the symbols,
            if (request.POST['tickerInput']).upper() in stockIndex:
                shares.append(request.POST['sharesOwned'])

                # adds inputed ticker to a list of user's stock tickers
                userStocks.append(request.POST['tickerInput'])

                # defines stock for the creation of the portEntry object
                #stock = Stock.objects.get(ticker=request.POST['tickerInput'])

                # creates portEntry object
                #portEntry = PortEntries.objects.create(stock=stock, sharesOwned=request.POST['sharesOwned'],\
                #user=request.user.username)
                # save object to models
                #portEntry.save()

                # load the next template because user is done inputing data
                template = loader.get_template('analyticals/stockDisplayView.html')

            # otherwise,
            else:
                # user entered an incorrect input
                input = False
                # reload same template until they get a correct input
                template = loader.get_template('analyticals/stockPickView.html')


        # the following is a list that will be used to hold data for a
        # template
        stockList = []

        # for each ticker (aka symbol) within the above list of stocks,
        for symbol in stockIndex:

            # assign stockQuote to specify which ticker to search for the API
            stockQuote = yf.Ticker(symbol)

            ticker = symbol

            companyName = str(stockQuote.info["shortName"])

            companyDescrip = str(stockQuote.info["longBusinessSummary"])

            # assign stockQuote to specify which ticker to search for the API
            stockQuote = yf.Ticker(symbol)

            # get the stock price of that stock from the API
            stockPrice = float(stockQuote.info["regularMarketOpen"])

            # get the fifty two week high from the API
            ftwh = float(stockQuote.info["fiftyTwoWeekHigh"])
            # get the fifty two week low from the API
            ftwl = float(stockQuote.info["fiftyTwoWeekLow"])

            stock = Stock.objects.create(ticker=ticker, companyName=companyName,\
            stockPrice=stockPrice, ftwh=ftwh, ftwl=ftwl, companyDescrip=companyDescrip)
            stock.save()

            stockList.append({'companyName': companyName,
                              'companyDescrip': companyDescrip,
                              'ticker': ticker,})


        context = {
            'stockIndex': stockIndex,
            'stockList': stockList,
            'shares': shares,
            'userStocks': userStocks,
            'input': input,
         }


        return HttpResponse(template.render(context, request))

    def get(self, request):
        template = loader.get_template('analyticals/urlErrorView.html')
        context = {}
        return HttpResponse(template.render(context, request))

class stockDisplayView(View):

    def post(self, request):
        # checks if the form submission was for logging out
        # because the user doesn't submit anything else when they log out, it
        # makes sense in terms of efficientcy to check if the user logged out first
        # instead of loading data which the user won't use
        if 'logoutButton' in request.POST.keys():
            # redirect to login view
            return redirect("loginView")

        context = {}
        return HttpResponse(template.render(context, request))

    def get(self, request):

        template = loader.get_template('analyticals/stockDisplayView.html')
        # put data in context for each view
        context = {}
        return HttpResponse(template.render(context, request))
