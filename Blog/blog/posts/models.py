from django.db import models
from django.core.urlresolvers import reverse

def upload_location(instance, filename):
	# filebase,extension = filename.split(".")
	# return "%s/%s.%s" %(instance.id,instance.id, extension)
	return "%s/%s" %(instance.id, filename)
class Post(models.Model):
	title = models.CharField(max_length=120)
	image = models.ImageField(	null=True, 
								blank=True, 
								upload_to = upload_location, 
								height_field ="height_field", 
								width_field="width_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"id":self.id})
		# return "/posts/%s/" %(self.id)
	class Meta(object):
		ordering = ["-timestamp","-updated"]