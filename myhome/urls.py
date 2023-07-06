from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.home, name="home"),
    path('business/',views.business),
    path('entertainment/',views.entertainment),
    path('health/',views.health),
    path('science/',views.science),
    path('sports/',views.sports),
    path('technology/',views.technology),
    path('sidebar_posts/',views.sidebar_posts),
    path('<str:category>/<int:post_id>/', views.post_detail, name='post_detail'), 
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),

]
