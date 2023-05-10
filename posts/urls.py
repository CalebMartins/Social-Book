from django.urls import path
from posts import views

urlpatterns = [
    path('upload-post/', views.upload_post, name='upload_post'),
    path('like/<post_id>', views.like, name='like')
]
