from django.urls import path
from main import views

# <follower_id>/<followed_id>

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('profile-page/<user_id>', views.profile, name='profile'),
    path('follow/', views.funllow, name='funllow'),
    path('search/', views.search, name='search')
]




