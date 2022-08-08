from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect as redirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from functools import wraps
from django.views.decorators.csrf import csrf_exempt



#Create a session
#TODO, when someone registers, append to People table and use that Id
@login_required
#Index for the user to view base page (active listings)
def index(request):
    content = Auction_Item.objects.all().values()
    return render(request, "auctions/index.html", 
    {
        "content": content, 
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(reverse("index"))
    
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")
    
#Login screen
def logout_view(request):
    logout(request)
    return redirect(reverse("index"))

#Register screen
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            person = People(name=username)
            user.save()
            person.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

#copypaste most of these implementations
#Create listing for item
def create_listing(request):
    if request.method == "POST":
        if request.POST.get("e", '') == '':
            return render(request, "auctions/failure.html")
        name = request.POST.get("a", '')
        price = request.POST.get("b", '')
        photo = request.POST.get("c", '')
        category = request.POST.get("d", '').lower()
        desc = request.POST.get("e", '')
        #Store in SQL
        #SELECT person_id FROM People WHERE name= request.user.username
        #get is an instance versus values which gives the value
        person = People.objects.filter(name=request.user.username).values('person_id')[0]["person_id"]
        a = Auction_Item(name=name, price=price, photo=photo, category=category, person_id=person, desc=desc)
        a.save()
        return render(request, "auctions/success.html")

    #easier and more tidy way is using "Create forms from models"
    #Copies from model and should autoupdate database
    return render(request, "auctions/create_listing.html")

#View Listing Page for specific item
def listing_page(request, id):
    content = Auction_Item.objects.filter(pk=id)
    comments = Comments.objects.filter(page_id=(Auction_Item.objects.filter(pk=id).values('id')[0]['id']))
    person = People.objects.filter(name=request.user.username).values('name')[0]["name"]
    return render(request, "auctions/listing_page.html", {
        "content": content,
        "comments": comments,
        "person": person,
    })

#View watchlist of items user wants to track
#TODO IF YOU EVER COME BACK GIVE PARAMATER NAME AND CHANGE DUDE59 TO NAME
def watchlist(request):
    #Check database for watchlist items
    watchlist = Watchlist.objects.filter(person=People.objects.get(name='Dude59')).select_related('person').select_related('watchlist')
    return render(request, "auctions/watchlist.html", {
        "watchlist" : watchlist,
    })

@csrf_exempt
def addwatch(request, id):
    #check database, populate
    #Watchlist(person=(People.objects.get(name='Dude59')), watchlist=(Auction_Item.objects.get(id='5'))) 
    
        try: 
            watchlist2 = Watchlist.objects.get(watchlist=Auction_Item.objects.get(id=id))  
            if int(watchlist2.watchlist.id) == int(id): 
                watchlist2.delete()
                print("Should be deleted")
                if request.method == "POST":
                    return JsonResponse({"Request": None})
                if request.method =="GET":
                    return watchlist(request)

        except Watchlist.DoesNotExist:
                watchlist2 = None
                
        watchlist1 = Watchlist(person=(People.objects.get(name=request.user.username)), watchlist=(Auction_Item.objects.get(id=id)))
        watchlist1.save()
        return JsonResponse({"Request": None})
    
    

def bid(request, id):
    #Check if bid higher or lower
    if request.method == "POST":
        item = Auction_Item.objects.filter(pk=id)
        price = item.values('price')[0]["price"]
        bid = int(request.POST.get("input0", ''))
        if price > bid:
            return JsonResponse({"response" : False})
        #update database
        item.update(price=bid)
        return JsonResponse({"response" : True})
    render(request, "auctions/failure.html")

    
   

def category(request, id):
    id = id.lower()
    content = Auction_Item.objects.filter(category=id)
    return render(request, "auctions/categories.html", {
        "content": content,
    })

def comment(request, id):
    if request.method == "POST":
        content = request.POST.get("input1", '')
        person = People.objects.filter(name=request.user.username).values('person_id')[0]["person_id"]
        auction = Auction_Item.objects.filter(pk=id).values('id')[0]["id"]
        comment = Comments(person_id=(person), page_id=(auction), text=content)
        comment.save()
        return JsonResponse({"response": True})
    render(request, "auctions/failure.html")
