from django.shortcuts import render,redirect, get_object_or_404
import requests
import requests
from datetime import datetime
from django.http import JsonResponse
from .models import Post
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Comment
from django.contrib.auth.decorators import login_required
from .models import Comment, Post


def is_valid_image_url(url):
    try:
        response = requests.head(url)
        content_type = response.headers.get('content-type')
        if content_type:
            return content_type.startswith('image/')
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def get_category_news(requested_category,sorted="published_desc",date=None,sidebar_post=False,limit=100,):
    api_key = "fc22b8b97fa327b1666d2f41d1826534"
    endpoint = "http://api.mediastack.com/v1/news"
    params = {
    "access_key": api_key,
    "limit":limit,
    "sort":sorted,
    "date":date,
    "categories":requested_category,
}
    # Send the HTTP GET request
    response = requests.get(endpoint, params=params)

    # Process the response
    if response.status_code == 200:
        news = response.json()['data']
        category_posts = []
        titles = {}
        if sidebar_post == True:
            #set length of news only for 5 times 
            news = news[:50]
        for new in news: 
            if new['title'] in titles:
                continue 
            else: 
                if new['image']:
                    # if is_valid_image_url(new['image']):
                    author = new['author']
                    title = new['title']
                    description = new['description']
                    category = new['category']
                    image = new['image']
                    exists = Post.objects.filter(title=title).exists()
                    post_data = {
                        'author': author,
                        'title': title,
                        'category': category,
                        'image':image,
                        'description': description
                    }
                    if exists:
                        post = Post.objects.get(title=title)
                        post_data['id'] = post.id 
                        category_posts.append(post)
                        titles[post_data['title']] = True 
                        continue
                    else:
                        post = Post(title=title,description=description,category=category,image=image,author=author)
                        post.save()
                        post_data['id'] = post.id 
                        category_posts.append(post_data)
                        titles[post_data['title']] = True 
                else:
                    continue
        
        return category_posts[::-1] if sidebar_post == False else category_posts
    else:
        print("failed !")
        return {}

# Create your views here.

def sidebar_posts(request):
    topic = request.GET.get('topic')
    category = request.GET.get('category')
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    date = "{}-{}-{}".format(currentYear,currentMonth,currentDay)
    days = '{}-{}-{},{}-{}-{}'.format(currentYear,currentMonth,currentDay,currentYear,currentMonth-1,currentDay)
    if topic == 'recent':
        if category == "general":
            sidebar_posts =  get_category_news('general',date=days,sidebar_post=True,limit=20)
        if category == "business":
            sidebar_posts =  get_category_news('business',date=days,sidebar_post=True,limit=20)
        if category == "entertainment":
            sidebar_posts =  get_category_news('entertainment',date=days,sidebar_post=True,limit=20)
        if category == "health":
            sidebar_posts =  get_category_news('health',date=days,sidebar_post=True,limit=20)
        if category == "science":
            sidebar_posts =  get_category_news('science',date=days,sidebar_post=True,limit=20)
        if category == "sports":
            sidebar_posts =  get_category_news('sports',date=days,sidebar_post=True,limit=20)
        if category == "technology":
            sidebar_posts =  get_category_news('technology',date=days,sidebar_post=True,limit=20)
    elif topic == 'popular':
        if category == "general":
            sidebar_posts =  get_category_news('general',date=days,sorted="popularity",sidebar_post=True,limit=20)
        if category == "business":
            sidebar_posts =  get_category_news('business',date=days,sorted="popularity",sidebar_post=True,limit=20)
        if category == "entertainment":
            sidebar_posts =  get_category_news('entertainment',date=days,sorted="popularity",sidebar_post=True,limit=20)
        if category == "health":
            sidebar_posts =  get_category_news('health',date=days,sorted="popularity",sidebar_post=True,limit=20)
        if category == "science":
            sidebar_posts =  get_category_news('science',date=days,sorted="popularity",sidebar_post=True,limit=20)
        if category == "sports":
            sidebar_posts =  get_category_news('sports',date=days,sorted="popularity",sidebar_post=True,limit=20)
        if category == "technology":
            sidebar_posts =  get_category_news('technology',date=days,sorted="popularity",sidebar_post=True,limit=20)
    response = []
    for post in sidebar_posts :
        image = post.image
        title = post.title
        id = post.id
        category = post.category
        response.append(
            {
                "sidebar-post-image":image,
                "sidebar-post-title":title,
                "sidebar-post-id":id,
                "sidebar-post-category":category,

            }
        )
    return JsonResponse({'response':  response})

def post_detail(request, category, post_id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = "Your name"
        post = Post.objects.get(category=category, id=post_id)
        comments = Comment.objects.filter(post_id=post.id)
        context = {'post': post, 'username': username, "comments":comments}
        return render(request, 'posts/post_detail.html', context)

    if request.method == 'POST':
        user_comment = request.POST.get("content")
        username = request.user.username
        post = get_object_or_404(Post, category=category, id=post_id)

        comment = Comment(content=user_comment, post=post, user=request.user)
        comment.save()
        comments = Comment.objects.filter(post_id=post.id)
        context = {'post': post, 'username': username, "comments":comments}

        return render(request, 'posts/post_detail.html', context)

def home(request):
    general_posts = get_category_news("general")
    return render(request,"pages/home.html",{"general_posts":general_posts})
    # return render(request,"pages/home.html")


    
def business(request):
    business_posts = get_category_news("business")
    return render(request,"pages/business.html",{"business_posts":business_posts})


def entertainment(request):
    entertainment_posts = get_category_news("entertainment")
    return render(request,"pages/entertainment.html",{"entertainment_posts":entertainment_posts})

def health(request):
    health_posts = get_category_news('health')
    return render(request,"pages/health.html",{"health_posts":health_posts})
    # return render(request,"pages/health.html")


def science(request):
    science_posts = get_category_news("science")
    return render(request,"pages/science.html",{"science_posts":science_posts})


def sports(request):
    sports_posts = get_category_news("sports")
    return render(request,"pages/sports.html",{"sports_posts":sports_posts})


def technology(request):
    technology_posts = get_category_news("technology")
    return render(request,"pages/technology.html",{"technology_posts":technology_posts})
    # return render(request,"pages/technology.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your home page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your home page
    return render(request, 'registration/register.html')