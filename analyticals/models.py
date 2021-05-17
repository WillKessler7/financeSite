from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Stock(models.Model):
    """
    This model will contain the data for the Stocks(ticker, stockprice, 52 week
    high, 52 week low)
    """

    ticker = models.CharField(max_length=5)
    companyName = models.CharField(max_length=50)
    stockPrice = models.DecimalField(max_digits=10, decimal_places=2)
    # 52 week high
    ftwh = models.DecimalField(max_digits=10, decimal_places=2)
    # 52 week low
    ftwl = models.DecimalField(max_digits=10, decimal_places=2)
    dateAdded = models.DateTimeField('date published')


    pass

class PortEntries(models.Model):
    """
    This model tracks the things that are specific to the user's portfolio
    rather than the general stock, the data it contains are the number of
    shares that each individual user has of a stock, which user bought this
    stock(which is a foriegnKey), and which stock it is(also a foriegnKey)
    """
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    sharesOwned = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    pass
