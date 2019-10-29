from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(PointsUser)
admin.site.register(PointsToDonateMonthBalance)
admin.site.register(PointsOwnedTransaction)