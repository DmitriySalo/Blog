from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Post



def post_list(request):
	queryset = Post.objects.all()
	context = {
		"object_list": queryset,
		"title": "User list",

	}

	# if request.user.is_authenticated():
	# 	context = {
	# 		"title":"User list"

	# 	}
	# else:
	# 	context = {
	# 		"title":"List"

	# 	}
	
	return render(request, 'blog/index.html',context)
	#return HttpResponse("<h1>List</h1>")
def post_create(request):
	return HttpResponse("<h1>Create</h1>")

def post_detail(request,id):
	#instance = Post.objects.get(id=1)
	instance = get_object_or_404(Post, id=id)
	context = {

		"title":"Detail",
		"instance": instance
	}
	return render(request, 'blog/post_detail.html',context)

def post_update(request):
	return HttpResponse("<h1>update</h1>")

def post_delete(request):
	return HttpResponse("<h1>delete</h1>")