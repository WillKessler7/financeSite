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

        # edit is assigned to false because the user most of time is not
        # requesting to edit
        edit = False

        # defines newUser as an empty string to initialize var
        newUser = ""

        # if the user clicked on the edit button in the display view,
        if 'edit' in request.POST.keys():
            # set edit to true for the template
            edit = True
            template = loader.get_template('analyticals/stockLoadView.html')
            context = {'edit': edit}

        # otherwise,
        else:
            # save the username and password data from template
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
                'edit': edit,
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
        userShares = []

        # list of tickers of stocks that user owns
        userStocks = []

        # this var indicates if the user has failed to correctly enter a ticker
        input = True

        # initializes a variable used in a for loop later
        stockQuote = ""

        # the following is a list that will be used to hold the index's stock
        # data for the stockPickView
        stockList = []

        # this is a list that will be used to hold the users data in stockDisplayView
        stockUserList = []

        # sets variable to display the number of users on the site
        numUsers = len(User.objects.all())

        # initializes a variable for the accumulator
        portfolioValue = 0



        """ program will iterate through the QQQ stock index and will show the
        stock ticker and company name to the user and the user can select if
        they want to follow the stock and view its information """

        # QQQ stock Index stocks that have full data with API
        #### NOTE: I shortened the list to make it easier to run but you can
        #### add the rest of the list
        stockIndex = ["THO", "MSFT", "AAPL", "AMZN", "FB", "GOOGL", "GOOG", "NFLX",\
        "NVDA", "PEP"]


        """, "ADBE", "CSCO", "PYPL", "TSLA", "AMGN", "COST",\
        "AVGO", "TXN", "GILD", "QCOM", "SBUX", "TMUS", "INTU", "FISV",\
        "ADP", "AMD", "REGN", "BKNG", "ATVI", "BIIB", "CSX",
        "ILMN", "JD", "ADSK", "ADI", "MELI", "WBA", "KHC", "LRCX", "EXC",\
        "EA", "EBAY", "ROST", "CTSH", "ORLY", "SGEN", "NXPI",\
        "BIDU", "MAR", "KLAC", "WDAY", "VRSK", "SIRI", "NTES", "VRSN",\
        "CSGP", "PCAR", "SNPS", "ANSS", "CDNS", "SPLK", "CTAS", "FAST",\
        "XLNX", "INCY", "CERN", "MCHP", "CPRT", "CTXS", "SWKS", "DLTR", "BMRN",\
        "ZM", "CHKP", "CDW", "TTWO", "MXIM", "ULTA", "WDC", "NTAP", "FOXA"]"""



        # if the button clicked was to load the data,
        if 'load' in request.POST.keys():
            # load the same template
            template = loader.get_template('analyticals/stockPickView.html')

        # otherwise, the only other button that could have been clicked at this
        # is the point is the submit button, so, the user is submitting,
        else:

            # split the data sent from the template into a list
            listOfSymbols = request.POST['symbolsInput']
            symbolList = listOfSymbols.split("|")

            # for every cluster of symbols in the list,
            for symb in symbolList:
                # strip all brackets and quotes from stringified object
                symb = symb.strip('"][')

                # split the list into a smaller list
                lineLst = symb.split(":")

                # if the inputs weren't empty and the ticker was an option in
                # the stock index
                if len(lineLst) == 2 and lineLst[0].upper() in stockIndex:
                    # try to save numShares  to an integer and other variables
                    try:
                        numShares = int(lineLst[1])
                        tickerSymbol = lineLst[0].upper()
                        userShares.append(numShares)
                        userStocks.append(tickerSymbol)

                    # if a value error is raised when trying to convert numShares
                    # to an integer, the input was incorrect
                    except ValueError:
                        input = False

                # otherwise,
                else:
                    input = False

            # if the user incorrectly entered one of their stocks,
            if input == False:
                # reload same view because input was incorrect
                template = loader.get_template('analyticals/stockPickView.html')

            # otherwise, if they correctly inputed their stock picks,
            else:

                # for every ticker or symbol that the user selected,
                for i in range(len(userStocks)):
                    # assign ticker to the symbol
                    ticker = userStocks[i]

                    # asssign the stock object as the last object within the list
                    # of queries
                    stockObj = Stock.objects.filter(ticker=ticker).last()

                    # get the stockPrice value from object
                    stockPrice = getattr(stockObj, "stockPrice")

                    ftwh = getattr(stockObj, "ftwh")

                    ftwl = getattr(stockObj, "ftwl")

                    # calculate the total value the user has of this stock
                    stockValue = userShares[i] * stockPrice

                    # accumulate the value of the user's portfolio
                    portfolioValue += stockValue

                    stockUserList.append({'ticker': ticker,
                                          'stockPrice': stockPrice,
                                          'ftwh': ftwh,
                                          'ftwl': ftwl,
                                          'stockValue': stockValue,
                                          })

                # load the next template because user is done inputing data
                template = loader.get_template('analyticals/stockDisplayView.html')

                context = {'stockUserList': stockUserList,
                           'numUsers': numUsers,
                           'portfolioValue': portfolioValue,
                }

                # send data and load template here so user doesn't have
                # to wait for the slow API call
                return HttpResponse(template.render(context, request))



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

            # assigns stock as a model object
            stock = Stock.objects.create(ticker=ticker, companyName=companyName,\
            stockPrice=stockPrice, ftwh=ftwh, ftwl=ftwl, companyDescrip=companyDescrip)
            # save the stock to models
            stock.save()

            # add the variables necessary for the stock pick view
            stockList.append({'companyName': companyName,
                              'companyDescrip': companyDescrip,
                              'ticker': ticker,
                              })



        context = {
            'stockIndex': stockIndex,
            'stockList': stockList,
            'userShares': userShares,
            'userStocks': userStocks,
            'input': input,
            'stockUserList': stockUserList,
            'numUsers': numUsers,
            'portfolioValue': portfolioValue,

         }


        return HttpResponse(template.render(context, request))

    def get(self, request):
        template = loader.get_template('analyticals/urlErrorView.html')
        context = {}
        return HttpResponse(template.render(context, request))

class stockDisplayView(View):

    def post(self, request):
        # checks if the form submission was for logging out
        if 'logoutButton' in request.POST.keys():
            # redirect to login view
            return redirect("loginView")

        context = {}
        return HttpResponse(template.render(context, request))

    def get(self, request):

        template = loader.get_template('analyticals/urlErrorView.html')
        # put data in context for each view
        context = {}
        return HttpResponse(template.render(context, request))
