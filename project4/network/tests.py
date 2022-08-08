from django.test import Client, TestCase
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
import json

#Write failing test, write enough code to make it pass. Then if you modify it later and functionality is gone you're notified
# Create your tests here.
#TODO Find a way to have request.user.username work, look into authenticate

class ViewsTestCase(TestCase):

    def setUp(self):

        #Create dummy data
        user0 = User.objects.create_user('Popzix', 'popi89ferezzx@gmail.com', 'scoop')
        user1 = User.objects.create_user('Dude59', 'dude59@gmail.com', 'dood')
        person0 = People.objects.create(name="Popzix", followers=0, desc="a bushel0 of well-kept apples!", user=(User.objects.get(username='Popzix')))
        person1 = People.objects.create(name="Dude59", followers=0, desc="a bushel1 of well-kept apples!", user=(User.objects.get(username='Dude59')))
        Popzix = (People.objects.get(name='Popzix'))
        Dude59 = (People.objects.get(name='Dude59'))
        post0 = Posts.objects.create(text="apple2", person=(Popzix), likes=0)
        post1 = Posts.objects.create(text="apple3", person=(Dude59), likes=0)
        follower0 = Followers.objects.create(followed=(Popzix), follower=(Dude59))

    #Test Each Model for expected storage
    def test_index(self):
        c = Client()
        response = c.get('')
        self.assertEqual(response.status_code, 200)

    #If submitting to github come back with guaranteed to fail tests
    #TODO First pass, make sure everything responds with 200
    #TODO Second pass, Make sure that whatever it sends back is actually what it's supposed to be
    #TODO Third pass, Go on front end and test that everything works as expected with Selenium

    def test_posts(self):
        Popzix = (People.objects.get(name='Popzix'))
        c = Client()
        c.login(username='Popzix', password='scoop')
        #POST
        response = c.post("/posts", {"body" : ["filler_text"]})
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response["response"], True)
        #EDIT
        post0 = Posts.objects.get(person=Popzix, text="apple2")
        response = c.post(f"/edit/{post0.id}", {"edit" : ["filler_text"]})
        self.assertEqual(response.status_code, 200)
        #PUT
        response = c.put("/posts")
        self.assertEqual(response.status_code, 200)

    def test_create_profile(self):
        #This should give an integrity error
        Popzix = (People.objects.get(name='Popzix'))
        c = Client()
        c.login(username='Popzix', password='scoop')
        #POST
        response = c.post("/create", {"desc" : ["peanut butter"]})
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        Popzix = (People.objects.get(name='Popzix'))
        c = Client()
        c.login(username='Popzix', password='scoop')
        #GET
        response = c.get("/profile/Popzix")
        self.assertEqual(response.status_code, 200)
        #PUT
        response = c.put("/profile/Popzix")
        self.assertEqual(response.status_code, 200)
        


    def test_following(self):
        c = Client()
        c.login(username='Popzix', password='scoop')
        #POST
        response = c.post("/Popzix/following/0")
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response["response"], True)
        #PUT
        response = c.put("/Dude59/following/1")
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response["pages"][0]["person"]["name"], 'Popzix')
        self.assertEqual(response["number"], 1)
        
        

    def test_like(self):
        Popzix = (People.objects.get(name='Popzix'))
        Dude59 = (People.objects.get(name='Dude59'))
        post1 = Posts.objects.create(text="apple3", person=(Dude59), likes=0)
        c = Client()
        c.login(username='Popzix', password='scoop')
        
        #GET
        response = c.get(f"/like/{post1.id}")
        self.assertEqual(response.status_code, 200)
        #POST
        response = c.post(f"/like/{post1.id}")
        self.assertEqual(response.status_code, 200)
        #PUT
        response = c.put(f"/like/{post1.id}")
        self.assertEqual(response.status_code, 200)


