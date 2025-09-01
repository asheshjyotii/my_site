from django.shortcuts import render

# Create your views here.

def home(req):
    return render(req, 'blog/home.html')

def posts(req):
    return render(req, 'blog/posts_page.html')

def particular_post(req, slug):
    return render(req, f'blog/posts/{slug}.html')