from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SettingForm
from .models import FollowerCount
from posts.models import Post
from authentication.models import Profile
import random

# Create your views here.
@login_required(login_url='signin/')
def index(request):
    posts = get_post_feed(request.user)
    users_to_follow = recommend_people(request.user)
    profile = Profile.objects.get(user=request.user)
    context = {'profile': profile, 'posts': posts, 'recommended': users_to_follow}
    return render(request, 'main/index.html', context)

def get_post_feed(current_user):
    following = FollowerCount.objects.filter(follower=current_user.username)
    following_list = [User.objects.get(username=person.user) for person in following]
    following_list.append(current_user)
    posts = Post.objects.filter(user__in = following_list).order_by('-date_posted')

    return posts

def recommend_people(current_user):
    following = FollowerCount.objects.filter(follower=current_user.username)
    following_list = [User.objects.get(username=person.user).id for person in following]
    following_list.append(current_user.id)
    recommended_users = User.objects.exclude(id__in = following_list)
    num = 5
    while True:
        try:
            li = random.sample(list(recommended_users), num)
            if li:
                break
        except:
            num -= 1
            continue
    recommended_users_dict = {user: FollowerCount.objects.filter(user=user.username).count() for user in li}
    
    return recommended_users_dict

@login_required(login_url='signin/')
def settings(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = SettingForm(request.POST, request.FILES)
        if form.is_valid():
            profile.profile_img = form.cleaned_data['profile_img']
            profile.bio = form.cleaned_data['bio']
            profile.location = form.cleaned_data['location']
            profile.save()
    else:
        form = SettingForm(
            {
                'bio' : profile.bio,
                'location': profile.location,
            }
        )
    context = {'form': form}
    return render(request, 'main/setting.html', context)

@login_required(login_url='signin/')
def profile(request, user_id):
    user = User.objects.get(id=int(user_id))
    posts = Post.objects.filter(user=user)
    following_check = FollowerCount.objects.filter(follower=request.user.username, user=user.username)
    num_of_followers = FollowerCount.objects.filter(user=user.username).count()
    num_following = FollowerCount.objects.filter(follower=user.username).count()
    if following_check:
        following = True
    else:
        following = False
    context = {'user': user, 'posts': posts, 
    'num_of_posts': len(posts), 'following': following,
    'followers': num_of_followers, 'following_num': num_following,}
    return render(request, 'main/profile.html', context)

@login_required(login_url='signin/')
def funllow(request):
    follower_id = request.GET.get('follower_id')
    followed_id = request.GET.get('followed_id')

    follower_user = User.objects.get(id=follower_id).username
    followed_user = User.objects.get(id=followed_id).username

    # print(follower_id)
    # print(followed_id)
    
    following_check = FollowerCount.objects.filter(follower=follower_user, user=followed_user)
    if following_check:
        following_check.delete()
    else:
        new_follower = FollowerCount(follower=follower_user, user=followed_user)
        new_follower.save()
        
    return redirect(f'/profile-page/{followed_id}')

@login_required(login_url='signin/')
def search(request):
    if request.method == 'POST':
        username = request.POST['username']
        users = User.objects.filter(username__icontains = username)
        print(users)
        if users:
            profile_list = [Profile.objects.get(user=user) for user in users if user.is_staff != 1 and user != request.user]
        else:
            profile_list = []
    context = {'profiles': profile_list, 'username': username}
    return render(request, 'main/search.html', context)
