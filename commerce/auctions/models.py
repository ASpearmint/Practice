from django.contrib.auth.models import AbstractUser
from django.db import models

#Never name a foreign key with _id because Django uses that to store an instance of the object
#You can access your id from person_id after creating person, person is now an instance storage
#An instance is the entire object itself data and all

class User(AbstractUser):
    pass

class Comments(models.Model):
    comments_id = models.AutoField(primary_key=True)
    #null for debug
    person = models.ForeignKey('People', on_delete=models.SET_NULL, related_name='comment', null=True)
    page = models.ForeignKey('Auction_Item', on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"Id: {self.comments_id}, person_id: {self.person_id}, text: {self.text}"
    
class Bids(models.Model):
    bid_id = models.AutoField(primary_key=True)
    person = models.ForeignKey('People', on_delete=models.CASCADE, related_name='bid', null=True)
    bids = models.IntegerField(null=True)
    page = models.ForeignKey('Auction_Item', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Id: {self.bid_id}, Item_id: {self.page_id} person_id: {self.person_id}, bids: {self.bids}"

class People(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, null=True)
    def __str__(self):
        return f"Person_id: {self.person_id}, name: {self.name}"

class Watchlist(models.Model):
    watchlist = models.ForeignKey('Auction_Item', on_delete=models.SET_NULL, null=True, related_name="Item")
    person = models.ForeignKey('People', on_delete=models.SET_NULL, null=True, related_name='watchlist') 
    def __str__(self):
        return f"Watchlist: {self.watchlist}, person: {self.person}"

class Auction_Item(models.Model):
    name = models.CharField(max_length=60, null=True)
    price = models.IntegerField(null=True)
    photo = models.CharField(max_length=5000, null=True)
    category = models.CharField(max_length=20, null=True)
    desc = models.CharField(max_length=3000, null=True)
    person = models.ForeignKey('People', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Name: {self.name}, price: {self.price}, photo: {self.photo}, category: {self.category} , person_id: {self.person_id}, desc: {self.desc}"
    




