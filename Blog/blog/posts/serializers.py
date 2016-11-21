from .models import Post
from rest_framework import serializers


class BlogSerializer(serializers.ModelSerializer):
	# post = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
	class Meta:
		model = Post
		fields = ('id','title','image','content')
