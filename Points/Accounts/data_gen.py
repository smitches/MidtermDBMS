from .models import *
from datetime import datetime
import calendar
import random

def add_points(user, points, date):
	exp_year = date.year
	exp_month = date.month
	exp_day = calendar.monthrange(exp_year, exp_month)[1]
	PointsToDonateMonthBalance(
		date_begin = date, 
		date_expire = datetime(month=exp_month, day=exp_day, year=exp_year),
		points_remaining=points,
		owner = user
		).save()

def give_users_points_todonate():
	for user in PointsUser.objects.all():
		add_points(user, 1000, datetime(month = 9, day = 1, year = 2019))
		add_points(user, 1000, datetime(month = 10, day = 1, year = 2019))

def add_donation(owner, donator, amount, date):
	PointsOwnedTransaction(owner = owner, donator= donator, amount_transacted = amount, date_transacted = date).save()
	donatebalance = user.pointstodonatemonthbalance_set.filter(date_expire__gte = date, date_begin__lte=date).first()
	donatebalance.points_remaining -= amount
	donatebalance.save()

def make_donations():
	users = PointsUser.objects.all()
	for month in (9,10):
		for user in users:
			amount_rem = 1000
			other_users = [x for x in users if x!= user]
			for i in range(3):
				rec_id = random.randint(0,len(other_users)-1)
				amount = random.randint(1, amount_rem)
				day = random.randint(1,30)
				add_donation(
					donator = user,
					owner = other_users[rec_id],
					amount = amount,
					date = datetime(month=month, day = day, year =2019)
					)

def spend_transaction(owner, amount, date):
	PointsOwnedTransaction(owner = owner, amount_transacted = amount, date_transacted = date).save()

def make_spend_txs(year):
	users = PointsUser.objects.all()
	dates = []
	for user in users:
		for month in (9,10):
			for day in range(1,calendar.monthrange(year, month)[1]+1):
				print('day')
				spend_choice = random.randint(0, 100)
				balance = user.get_spendable_balance()
				if spend_choice <= balance/100 and balance > 100:
					spend_transaction(user, -100, datetime(month=month, day=day, year=year))

def main():
	# give_users_points_todonate()
	# make_donations()
	# make_spend_txs(2019)
	pass