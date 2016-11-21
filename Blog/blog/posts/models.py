from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
	# filebase,extension = filename.split(".")
	# return "%s/%s.%s" %(instance.id,instance.id, extension)
	return "%s/%s" %(instance.id, filename)
class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique = True)
	image = models.ImageField(	null=True, 
								blank=True, 
								upload_to = upload_location, 
								height_field ="height_field", 
								width_field="width_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateTimeField(auto_now=False, auto_now_add=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager()


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"id":self.id})
		# return "/posts/%s/" %(self.id)
	class Meta(object):
		ordering = ["-timestamp","-updated"]


def pre_save_post_receiver(sender,instance,*args,**kwargs):
	slug  = slugify(instance.title)
	exists = Post.objects.filter(slug=slug).exists()
	if exists:
		slug = "%s-%s" %(slug,instance.id)
	instance.slug = slug
pre_save.connect(pre_save_post_receiver, sender=Post)