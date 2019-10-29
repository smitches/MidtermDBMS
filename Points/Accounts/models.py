from django.db import models

from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
## our user class inherit from user or have a foreign key to user
class PointsUser(User):
	admin = models.BooleanField(default=False)

##one gets created per user per month
class PointsToDonateMonthBalance(models.Model):
	points_remaining = models.IntegerField()
	owner = models.ForeignKey(PointsUser, on_delete = models.CASCADE)
	date_begin = models.DateTimeField(default=datetime.now, blank=True)
	date_expire = models.DateTimeField(default=datetime.now, blank=True)
	def __str__(self):
		return str(self.owner) + ' has ' + str(self.points_remaining) + ' expiring ' + str(self.date_expire)

class PointsOwnedTransaction(models.Model):
	owner = models.ForeignKey(PointsUser, on_delete = models.CASCADE, related_name='owner')
	donator = models.ForeignKey(PointsUser, on_delete=models.CASCADE, blank=True, null=True, related_name='donator')
	date_transacted = models.DateTimeField(default=datetime.now, blank=True)
	amount_transacted = models.IntegerField(default=0) ## NEGATIVE FOR SPEND, POSITIVE FOR RECEIVE
	def __str__(self):
		if self.amount_transacted > 0:
			return (str(self.owner) + ' received ' + str(self.amount_transacted) + 
				' from ' + str(self.donator)+ ' on ' + str(self.date_transacted))
		return (str(self.owner) + ' spent ' + str(self.amount_transacted) + 
				' on ' + str(self.date_transacted))


# create a transaction of tanvi gives brian 100 (brian owner, donator tanvi, +100)
# simultaneously, PointsToDonateMonthBalance is reduced 100