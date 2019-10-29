from .models import *
from datetime import datetime
import calendar
import random

def add_points(user, points, date):
	exp_year = date.year
	exp_month = date.month
	exp_day = calendar.monthrange(exp_year, exp_month)[1]
	donate_balance = PointsToDonateMonthBalance(
		date_begin = date, 
		date_expire = datetime(month=exp_month, day=exp_day, year=exp_year),
		points_remaining=points,
		owner = user
		)
	donate_balance.save()

def give_users_points():
	for user in PointsUser.objects.all():
		add_points(user, 1000, datetime(month = 9, day = 1, year = 2019))
		add_points(user, 1000, datetime(month = 10, day = 1, year = 2019))

def add_transaction(owner, donator, amount, date):
	PointsOwnedTransaction(owner = owner, donator= donator, amount_transacted = amount, date_transacted = date).save()

def make_transactions():
	users = PointsUser.objects.all()
	for month in (9,10):
		for user in users:
			amount_rem = 1000
			other_users = [x for x in users if x!= user]
			for i in range(3):
				rec_id = random.randint(0,len(other_users)-1)
				amount = random.randint(1, amount_rem)
				day = random.randint(1,30)
				add_transaction(
					donator = user,
					owner = other_users[rec_id],
					amount = amount,
					date = datetime(month=month, day = day, year =2019)
					)


def main():
	# give_users_points()
	make_transactions()

# class PointsUser(User):
# 	admin = models.BooleanField(default=False)

# ##one gets created per user per month
# class PointsToDonateMonthBalance(models.Model):
# 	points_remaining = models.IntegerField()
# 	owner = models.ForeignKey(PointsUser, on_delete = models.CASCADE)
# 	date_begin = models.DateTimeField(default=datetime.now, blank=True)
# 	date_expire = models.DateTimeField(default=datetime.now, blank=True)
# 	def __str__(self):
# 		return str(self.owner) + ' has ' + str(self.points)

# class PointsOwnedTransaction(models.Model):
# 	owner = models.ForeignKey(PointsUser, on_delete = models.CASCADE, related_name='owner')
# 	donator = models.ForeignKey(PointsUser, on_delete=models.CASCADE, blank=True, null=True, related_name='donator')
# 	date_transacted = models.DateTimeField(default=datetime.now, blank=True)
# 	amount_transacted = models.IntegerField(default=0) ## NEGATIVE FOR SPEND, POSITIVE FOR RECEIVE
