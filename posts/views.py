from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post, Like
from uuid import UUID

# Create your views here.
@login_required(login_url='signin/')
def upload_post(request):
    if request.method == 'POST':
        print(request.FILES.get('image_upload'))
        new_post = Post(
            user = request.user,
            caption = request.POST['image_caption'],
            image = request.FILES.get('image_upload')
        )
        new_post.save()
    else:
        pass
    
    return redirect('/')

@login_required(login_url='signin/')
def like(request, post_id):
    post = Post.objects.get(id=UUID(post_id))
    like = Like.objects.filter(user=request.user, post=post).first()
    if like:
        like.delete()
    else:
        Like.objects.create(post=post, user=request.user)
    return redirect('/')

