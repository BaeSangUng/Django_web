from django.shortcuts import render
from .models import Post
# Create your views here.


def index(request): # request는 기본이므로 건드는 거x
    posts = Post.objects.all()     # Post에서 모든걸 가져와라 (django 제공)
    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
        }
    )
    