from django.urls import path
from .import views
urlpatterns = [
    path('home/',views.home),
    path('sports/',views.sports),
    path('technology/',views.technology),

]
