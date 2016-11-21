from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.six.moves.urllib.parse import quote_plus
from django.utils import timezone
from django.db.models import Q

def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()
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
		"today": today,

	}

	
	return render(request, 'blog/post_list.html',context)
	#return HttpResponse("<h1>List</h1>")
def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	# if not request.user.is_authenticated():
	# 	raise Http404

	form =PostForm(request.POST or None, request.FILES or None )
	# if request.method == 'POST':
	# 	print (request.POST.get("content"))
	# 	print (request.POST.get("title"))
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
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
	if instance.publish > timezone.now() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	context = {

		"title":"Detail",
		"instance": instance,
		"share_string": share_string,
	}
	return render(request, 'blog/post_detail.html',context)

def post_update(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
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
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request,"Successfully deleted")
	return redirect("posts:list")

