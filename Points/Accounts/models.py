from django.db import models

from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
## our user class inherit from user or have a foreign key to user
class PointsUser(User):
	admin = models.BooleanField(default=False)
	def __str__(self):
		return self.username + ': Received: {}, Spent: {}'.format(self.get_total_received(), self.get_total_spent())
	def get_spendable_balance(self):
		return self.owned_points_set.aggregate(models.Sum('amount_transacted'))['amount_transacted__sum']
	def get_total_spent(self):
		return self.owned_points_set.filter(amount_transacted__lt=0).aggregate(models.Sum('amount_transacted'))['amount_transacted__sum']
	def get_total_received(self):
		return self.owned_points_set.filter(amount_transacted__gt=0).aggregate(models.Sum('amount_transacted'))['amount_transacted__sum']
	def get_donatable_balance(self):
		try:
			return self.pointstodonatemonthbalance_set.filter(date_expire__gte= datetime.now(), date_begin__lte=datetime.now()).first().points_remaining
		except:
			return 0

##one gets created per user per month
class PointsToDonateMonthBalance(models.Model):
	points_remaining = models.IntegerField()
	owner = models.ForeignKey(PointsUser, on_delete = models.CASCADE)
	date_begin = models.DateTimeField(default=datetime.now, blank=True)
	date_expire = models.DateTimeField(default=datetime.now, blank=True)
	def __str__(self):
		return str(self.owner) + ' has ' + str(self.points_remaining) + ' expiring ' + str(self.date_expire)

class PointsOwnedTransaction(models.Model):
	owner = models.ForeignKey(PointsUser, on_delete = models.CASCADE, related_name='owned_points_set')
	donator = models.ForeignKey(PointsUser, on_delete=models.CASCADE, blank=True, null=True, related_name='donation_set')
	date_transacted = models.DateTimeField(default=datetime.now, blank=True)
	amount_transacted = models.IntegerField(default=0) ## NEGATIVE FOR SPEND, POSITIVE FOR RECEIVE
	def __str__(self):
		if self.amount_transacted > 0:
			return (str(self.owner) + ' received ' + str(self.amount_transacted) + 
				' from ' + str(self.donator)+ ' on ' + str(self.date_transacted))
		return (str(self.owner) + ' spent ' + str(-1*self.amount_transacted) + 
				' on ' + str(self.date_transacted))

