from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm


def post_list(request):
	posts = BlogPost.objects.order_by("-created_at")
	return render(request, "blog/index.html", {"posts": posts})


def post_detail(request, pk):
	post = get_object_or_404(BlogPost, pk=pk)
	return render(request, "blog/detail.html", {"post": post})


def post_create(request):
	if request.method == "POST":
		form = BlogPostForm(request.POST)
		if form.is_valid():
			post = form.save()
			return redirect("blog:post_detail", pk=post.pk)
	else:
		form = BlogPostForm()

	return render(request, "blog/create.html", {"form": form})
