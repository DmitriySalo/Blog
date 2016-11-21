from .models import Post
from rest_framework import serializers


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title','image','content')
