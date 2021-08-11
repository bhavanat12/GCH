from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class TodoItem(models.Model):
	auto_inc_id = models.AutoField(primary_key=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return ('/')


class MapGeometry(models.Model):
	auto_inc = models.AutoField(primary_key=True)
	reviewer = models.TextField()
	mapItem = models.TextField()
	layer = models.TextField(default='https://services3.arcgis.com/nTlnK5Q4GIhY3A7b/arcgis/rest/services/docusign_hackathon/FeatureServer/0')
	datecreated = models.DateTimeField(auto_now_add=True)
	comments = models.TextField(default='Enter your comments here')

	def get_absolute_url(self):
		return ('/')

class CompletedMaps(models.Model):
	auto_inc = models.AutoField(primary_key=True)
	reviewer = models.TextField()
	mapItem = models.TextField()
	layer = models.TextField(default='https://services3.arcgis.com/nTlnK5Q4GIhY3A7b/arcgis/rest/services/docusign_hackathon/FeatureServer/0')
	dateSubmitted = models.DateTimeField(auto_now_add=True)
	comments = models.TextField(default='Enter your comments here')
	status = models.TextField()

class FinalMaps(models.Model):
	auto_inc = models.AutoField(primary_key=True)
	gisUser = models.ForeignKey(User, on_delete=models.CASCADE)
	mapItem = models.TextField()
	layerURL = models.TextField(default='https://services3.arcgis.com/nTlnK5Q4GIhY3A7b/arcgis/rest/services/docusign_hackathon/FeatureServer/0')
	dateSubmitted = models.DateTimeField(auto_now_add=True)
	approvalCount = models.IntegerField(default=0)
	reviewerReadable = models.TextField(default="False")


class ApprovedMap(models.Model):
	auto_inc = models.AutoField(primary_key=True)
	layerURL = models.TextField(default='https://services3.arcgis.com/nTlnK5Q4GIhY3A7b/arcgis/rest/services/docusign_hackathon/FeatureServer/0')
	mapItem = models.TextField()
	dateSubmitted = models.DateTimeField(auto_now_add=True)




