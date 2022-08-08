import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
#May need to change False and True to be JsonResponse or HttpResponse

def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def edit_post(request, id): 
    #POST for Edit Posts
    if request.method == "POST":
        try:
            user = (User.objects.get(username=request.user.username))
            person = People.objects.filter(user=user)
            if not person.exists():
                return render(request, "network/error.html", {"error": "Requires a response"}) 
            content = json.loads(request.body)
            content = content["edit"]
            text_post = Posts.objects.get(pk=id)
            text_post.text = content
            text_post.save()
            return JsonResponse({"response" : True})
        except KeyError:
            return render(request, "network/error.html", {"error": "Requires a person"})

@login_required
def posts(request):
    #POST for Creation
    if request.method == "POST":
        try:
            user = (User.objects.get(username=request.user.username))
            person = People.objects.get(user=user)
            content = request.POST["body"]
            text_post = Posts(text=content, person=person, likes=0)
            text_post.save()
            return HttpResponse(True)

        except ObjectDoesNotExist:
            return render(request, "network/error.html", {"error": "Requires a person"})
                
    #Put for Load Posts
    if request.method == "PUT":
        try: 
            posts = Posts.objects.all()
            content = posts.order_by("-timestamp").all()
            return JsonResponse([text.serialize() for text in content], safe=False)

        except ValueError:
            return render(request, "network/error.html", {"error": "Unknown"})

@login_required
def create_profile(request):
    #TODO Outside scope, but if creating profile that has already has user, should notify user returning some error response
    if request.method == "POST":
        try:
            desc = request.POST["desc"]
            person = People(name=request.user.username, followers=0, desc=desc, user=(User.objects.get(username=request.user.username)) )
            person.save()
            return JsonResponse({"response" : True})
        except IntegrityError:
            return render(request, "network/error.html", {"error": "Requires a response"})

#Profile Page 
@login_required
def profile(request, name):
        
    #Render target profile    
    if request.method == "GET":
        try:
            bio = ''
            bio = People.objects.get(name=name) 
            return render(request, "network/profile.html", {"bio": bio})

        #If not previously created, redirect to create a page
        except ObjectDoesNotExist:
            return render(request, "network/create_profile.html")

    #PUT to load own posts
    if request.method == "PUT":
        try: 
            person = People.objects.get
            user = User.objects.get
            posts = Posts.objects.filter(person=person(user=user(username=name)))
            content = posts.order_by("-timestamp").all()
            return JsonResponse([text.serialize() for text in content], safe=False)
        except ObjectDoesNotExist:
            return render(request, "network/error.html", {"error" : "Create a Profile before using that function!"})    

    return render(request, "network/error.html", {"error": "Method must be GET or PUT"})
   

@login_required
def following(request, name, page):
    #POST for following person
    if request.method == "POST":
        try:
            #Added to your followers list
            
            counter = People.objects.get(name=name)
            if not Followers.objects.filter(followed=People.objects.get(name=name), follower=People.objects.get(user=(User.objects.get(username=request.user.username)))).exists():
                following = Followers(followed=People.objects.get(name=name), follower=People.objects.get(user=(User.objects.get(username=request.user.username))))
                following.save()
                #You follow someone, they get a follower
                counter.followers =+1
                counter.save()
                return JsonResponse({"response" : True})
            counter.followers =- 1
            counter.save()
            instance = Followers.objects.get(followed=People.objects.get(name=name), follower=People.objects.get(user=(User.objects.get(username=request.user.username))))
            instance.delete()
            return JsonResponse({"response" : False})
        
        except ObjectDoesNotExist:
            return render(request, "network/error.html", {"error" : "Either you need to create a profile, or the person can no longer be followed"})  

    #PUT for loading on profile
    if request.method == "PUT":
     
        # Get post of every person followed by target profile person ordered by timestamp
        
        try: 
            followed = People.objects.get(name=name)

            followed = Followers.objects.filter(follower=People.objects.get(name=name))

            dynamic = ''

            for i, item in enumerate(followed):
                if i == 0:
                    dynamic = f"Q(person=People.objects.get(name=\"{item.followed.name}\"))"
                dynamic = f"Q(person=People.objects.get(name=\"{item.followed.name}\")) | {dynamic}"
                
            #This IS a solution but holy crap is it bad    
            followed = Posts.objects.filter(eval(dynamic)).order_by("-timestamp").all()
            
            #Paginate it
            followed = Paginator(followed, 10)
            pages = followed.page(page)
            pages = [page.serialize() for page in pages]
            return JsonResponse({"number" : followed.num_pages, "pages" : pages}, safe=False)
             
        except ObjectDoesNotExist:
            return JsonResponse({"response" : None})

       
        
        


@login_required
def like(request, id):
    #POST add a like
    if request.method == "POST":
        try: 
            posts = Posts.objects.get(pk=id)
            posts.likes =+ 1
            posts.save()
            return JsonResponse({"response" : True})
        except ObjectDoesNotExist:
             return render(request, "network/error.html", {"error": "Post not found"})
    #Get subtract a like
    if request.method == "GET":
        try:
            posts = Posts.objects.get(pk=id)                
            posts.likes =- 1
            posts.save()
            return JsonResponse({"response" : True})
        except: 
            return render(request, "network/error.html", {"error": "Post not found"})
    #Put access likes
    if request.method == "PUT":
        try: 
            likes = Posts.objects.get(pk=id).likes
            return JsonResponse({"likes": likes})
        except ObjectDoesNotExist:
            return render(request, "network/error.html", {"error": "Post not found"})

