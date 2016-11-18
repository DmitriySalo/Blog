from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def post_list(request):
	queryset_list = Post.objects.all()
	paginator = Paginator(queryset_list, 5) # Show 25 queryset per page
	page_request_var = 'post'
	page = request.GET.get(page_request_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list": queryset,
		"title": "User list",
		"page_request_var":page_request_var,

	}

	# if request.user.is_authenticated():
	# 	context = {
	# 		"title":"User list"

	# 	}
	# else:
	# 	context = {
	# 		"title":"List"

	# 	}
	
	return render(request, 'blog/post_list.html',context)
	#return HttpResponse("<h1>List</h1>")
def post_create(request):
	form =PostForm(request.POST or None, request.FILES or None )
	# if request.method == 'POST':
	# 	print (request.POST.get("content"))
	# 	print (request.POST.get("title"))
	if form.is_valid():
		instance = form.save(commit=False)
		# print(form.cleaned_data.get("title"))
		instance.save()
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {

		"form":form,
		
	}
	return render(request, 'blog/post_form.html',context)

def post_detail(request,id):
	#instance = Post.objects.get(id=1)
	instance = get_object_or_404(Post, id=id)
	context = {

		"title":"Detail",
		"instance": instance
	}
	return render(request, 'blog/post_detail.html',context)

def post_update(request, id=None):
	instance = get_object_or_404(Post,id=id)
	form =PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

		messages.success(request,"Successfully Update")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title":instance.title,
		"instance": instance,
		'form': form,
	}

	return render(request, 'blog/post_form.html',context)

def post_delete(request, id=None):
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request,"Successfully deleted")
	return redirect("posts:list")

