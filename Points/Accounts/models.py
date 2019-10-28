from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class PointsAccount(models.Model):
	points = models.IntegerField()
	owner = models.ForeignKey(User, on_delete = models.CASCADE)
	def __str__(self):
		return str(self.owner) + ' has ' + str(self.points)
