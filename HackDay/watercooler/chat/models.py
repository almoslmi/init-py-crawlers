from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here

class Channel(models.Model):
	name = models.CharField(max_length=30)
	number_of_users = models.IntegerField()
	
	def __str__(self):
		return "%s" %(self.name)

class ChatEntry(models.Model):
	chat_text = models.TextField()
	channel = models.ForeignKey(Channel)
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField()
	
	def __str__(self):
		return "%s %s %s: %s" %(str(self. timestamp), self.channel, self.user, self.chat_text)


