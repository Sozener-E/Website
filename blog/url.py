from django.urls import path
from .views import (
    PostApiView,
    PostDetailApiView
)

urlpatterns = [
    path('post/api', PostApiView.as_view()),
    path('post/<int:post_id>/', PostDetailApiView.as_view()),
]