from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    pass

class People(models.Model):
    name = models.CharField(max_length=100)
    followers = models.IntegerField()
    desc = models.CharField(max_length=3000, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"name: {self.name}, followers: {self.followers}, desc: {self.desc}"

    def serialize(self):
        return {
            "name" : self.name,
            "followers" : self.followers,
            "desc" : self.desc, 
        }

class Posts(models.Model):
    text = models.CharField(max_length=3000)
    timestamp = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey('People', on_delete=models.SET_NULL, related_name='Post', null=True)
    likes = models.IntegerField()

    def __str__(self):
        return f"text: {self.text}, person {self.person}, likes {self.likes}"

    def serialize(self): 
        return {
            "id" : self.id,
            "text" : self.text,
            "timestamp" : self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "person" : self.person.serialize(),
            "likes" : self.likes,
        }
    


class Followers(models.Model):
    #person followed
    followed = models.ForeignKey('People', on_delete=models.SET_NULL, related_name='Follower', null=True)
    #person following
    follower = models.ForeignKey('People', on_delete=models.SET_NULL, related_name='Following', null=True)

    def __str__(self):
        return f"followed: {self.followed} follower: {self.follower}"