from django.contrib import admin

from .models import *
# Register your models here.

register = admin.site.register

register(Auction_Item)
register(Comments)
register(People)
register(User)
register(Watchlist)
