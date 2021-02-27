from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related


class User(AbstractUser):
    pass

class Posts(models.Model):
    created_by = models.ForeignKey(User, on_delete = models.CASCADE)
    postContent = models.CharField(max_length = 256)
    dateAndTime = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return{
            "id" : self.id,
            "created_by" : self.created_by.username,
            "postContent" : self.postContent,
            "dateAndTime" : self.dateAndTime.strftime("%m/%d/%Y, %H:%M:%S"),
            "likes" : self.likes
        }


class LikesList(models.Model):
    likedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    idForPost = models.ForeignKey(Posts, on_delete=models.CASCADE, blank = True, null=True)



class Profile(models.Model):
    profileOwner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'owner', null=True) 
    followers = models.IntegerField(null = True)
    following = models.IntegerField(null = True)

class FollowingList(models.Model):
    listOwner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'listOwnerFIng', null=True) 
    followingID = models.ForeignKey(User, on_delete = models.CASCADE, related_name='followingList', null=True)

class FollowerList(models.Model):
    listOwner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'listOwnerF', null=True) 
    followerID = models.ForeignKey(User,  on_delete = models.CASCADE, related_name='followerList', null=True)    
