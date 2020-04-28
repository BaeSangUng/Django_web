from django.shortcuts import render
from .models import Post
from django.views.generic import ListView

class PostList(ListView):
    model = Post
    # created 순서의 반대로
    def get_queryset(self):
        return Post.objects.order_by('-created')
# 이 주석이 위에 두줄로 해결(django 기능)
# def index(request): # request는 기본이므로 건드는 거x
#     posts = Post.objects.all()     # Post에서 모든걸 가져와라 (django 제공)
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )
