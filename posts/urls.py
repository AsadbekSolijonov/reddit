from django.urls import path, include
from posts import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('group', views.GroupViewSet)

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostRetrieveDestroy.as_view()),
    path('posts/<int:pk>/vote/', views.VoteCreate.as_view()),
    path('', include(router.urls))
]


