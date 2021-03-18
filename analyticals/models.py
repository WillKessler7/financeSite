from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Stock(models.Model):
    """
    This model will contain the data for the Stocks(ticker, stockprice, 52 week
    high, 52 week low)
    """
    #return Stock
    pass

class portEntries(models.Model):
    """
    This model tracks the things that are specific to the user's portfolio
    rather than the general stock, the data it contains are the number of
    shares that each individual user has of a stock, which user bought this
    stock(which is a foriegnKey), and which stock it is(also a foriegnKey)
    """
    #return portEntries
    pass
