from django.shortcuts import render, redirect
from .forms import BlogForm
from .models import Blog
from .forms import LoginForm
import requests



def get_category_news(requested_category):
    api_key = "7d7be352708d73125a4ad5d9835a293c"
    endpoint = "http://api.mediastack.com/v1/news"
    params = {
    "access_key": api_key,
    "categories":requested_category
}
    # Send the HTTP GET request
    response = requests.get(endpoint, params=params)

    # Process the response
    if response.status_code == 200:
        news = response.json()['data']
        category_posts = []

        for new in news:
            author = new['author']
            print(author)
            title = new['title']
            description = new['description']
            category = new['category']
            image = new['image']
            sports_post = {
                'author': author,
                'title': title,
                'category': category,
                'image':image,
                'description': description
            }
            category_posts.append(sports_post)
        return category_posts
    else:
        return {}

# Create your views here.


def home(request):
    return render(request,"pages/home.html")

    
# def business(request):


# def entertainment(request):

# def health(request):

# def science(request):


def sports(request):
    sports_posts = get_category_news("sports")
    return render(request,"pages/sports.html",{"sports_posts":sports_posts})




def technology(request):
    technology_posts = get_category_news("sports")
    return render(request,"pages/sports.html",{"sports_posts":technology_posts})
