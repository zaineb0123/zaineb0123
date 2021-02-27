import json
from django.contrib.auth import authenticate, login, logout
from django.template.defaulttags import register
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.core.paginator import Paginator
from .models import User, Posts, Profile, FollowingList, FollowerList, LikesList
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def index(request):
    print("i am running")  
    # saving new tweet
    if request.method == 'POST':
        userName = request.user
        print("Username is ", userName)
        unsavedPost = request.POST.get("newPostBox")
        dataFromTweet = Posts()
        dataFromTweet.created_by = userName
        dataFromTweet.postContent = unsavedPost
        dataFromTweet.save()
        
        print("i am saving stuff")
        JsonResponse(dataFromTweet.serialize())
        
    
    allData = Posts.objects.all()
    allData = allData.order_by("-dateAndTime").all()
    print("I am displaying all posts")

    #Pagination
    paginator = Paginator(allData, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/index.html", {
        'page_obj': page_obj
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
             #create user profile as soon as a user registers
            print("USER NAME IS REGISTER IS ", username)
            userID = User.objects.get(username = username)
            print("User ID is", userID)
            userProfile = Profile()
            userProfile.profileOwner = userID
            userProfile.followers = 0
            userProfile.following = 0
            userProfile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
       

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

#prints the profile page, updates follow count and list
def profilePage(request, userName):
    print("I'm inside Profile Page")

     #get user ID against the username
    userID = User.objects.get(username = userName)
    # print("USER ID IS",userID)
    profileOwner = Profile.objects.get(profileOwner = userID)

      #get profileDetails as in posts of the user whose profile has been opened
    details = Posts.objects.filter(created_by = userID)
    details = details.order_by("-dateAndTime").all()

    #Pagination
    paginator = Paginator(details, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    #if user is signed in
    if request.user is None:
        loggedinUser = Profile.objects.get(profileOwner = request.user)
    
        followingCount = []
        followerCount = []

    

        #check if user is already following this profile
        checkIfFollowing = FollowerList.objects.filter(listOwner = userID, followerID = request.user)
        if checkIfFollowing:
            following = 1
        else:
            following = 0

        print("following is ", following)


        #update following count when follow button is clicked and save entry in FollowingList
        if request.method == 'POST':
            print("button clicked")
            print("checkIfFollowing", checkIfFollowing)

            if checkIfFollowing:
                print("Already following, so imma unfollow now")
                followerCount = profileOwner.followers - 1
                profileOwner.followers = followerCount
                FollowerList.objects.filter(listOwner = userID, followerID = request.user).delete()
                

                #decrease logged-in user's following count
                followingCount = loggedinUser.following - 1
                loggedinUser.following = followingCount
                FollowingList.objects.filter(listOwner = request.user, followingID = userID).delete()

                following = 0 #show Follow text on button


            else:
                print("NOT following, so imma follow now")
                followerCount = profileOwner.followers + 1
                profileOwner.followers = followerCount 
                updateFList = FollowerList(listOwner = userID, followerID = request.user)
                updateFList.save()
                

                #increase logged-in user's following count
                followingCount = loggedinUser.following + 1
                loggedinUser.following = followingCount
                updateFollowingList = FollowingList(listOwner = request.user, followingID = userID)
                updateFollowingList.save()

                following = 1 #show following/unfollow text on button



            profileOwner.save()
            loggedinUser.save()

        return render(request, "network/profilePage.html", {
            "profileOwner" : profileOwner, 
            "details": page_obj,
            "following": following
        })

    



    # print ("profile details", details)
    return render(request, "network/profilePage.html", {
        "profileOwner" : profileOwner, 
        "details": page_obj,
        
    })



#prints the posts on "Following" page
def following(request, userName):
    userProfiles = FollowingList.objects.filter(listOwner = request.user).all()
    print("userProfile is ", userProfiles)
    
    listOfAllPosts = []

    #get posts against following
    for uP in userProfiles:
        getPosts = Posts.objects.filter(created_by = uP.followingID)
        print("Value of getPosts is", getPosts)
        listOfAllPosts.append(getPosts)
        # listOfAllPosts.append(getPosts.values('created_by', 'postContent', 'dateAndTime'))

    #Pagination
    paginator = Paginator(listOfAllPosts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
            "listOfAllPosts" : page_obj
            })




@csrf_exempt
def editTweet(request, post_id):
    postData = Posts.objects.filter(id = post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        print("data value is ", data)
    
        #updating data in the database where id = post_id
        Posts.objects.filter(id = post_id).update(postContent = data.get('postContent', None))

        print ("i'm inside PUT")
        return render(request, 'network/index.html')
    else:    
        print("i'm inside else")
        return JsonResponse([post.serialize() for post in postData], safe=False)

    
@csrf_exempt
@login_required    
def likePost(request, post_id):
    post = Posts.objects.get(id = post_id)
    likesForPost = post.likes

#psuedo code
#I want to add and subtract likes from two tables. 
# 1. Like count in Posts
# 2. Likes List in LikesList


    print("atleast, I run")
  
    post = Posts.objects.get(id = post_id)
    print("post.id is ", post.id)
  
    likesForPost = post.likes
    print("likes at beginning ", likesForPost)

    likeDetailsTwo = LikesList.objects.filter(idForPost = post.id, likedBy = request.user)
    print("like Details", likeDetailsTwo)

    if post:
        print("INSIDE POST")
        if likeDetailsTwo: #user has already liked the post
            print("DISliking")
            #update the value of likes in posts table
            likesForPost = likesForPost - 1
            #updating count
            Posts.objects.filter(id = post.id).update(likes = likesForPost)
            print("likes after disliking ", likesForPost - 1)
            #removing row from LikesList
            LikesList.objects.filter(idForPost = post.id, likedBy = request.user).delete()
    
        else:
            #update the value of likes in posts table
            likesForPost = likesForPost + 1
            #updating likes in Posts
            Posts.objects.filter(id = post_id).update(likes = likesForPost)
            
            print("Liking")
            print("request.user", request.user)
            print("post", post) 
           
            #adding row in Likes List
            likeDetailsThree = LikesList(likedBy = request.user, idForPost = post)
            print("likeDetailsThree", likeDetailsThree)
            likeDetailsThree.save()
            print("likes after LIKING ", likesForPost)
            print("SAVED!")
            # post.likes = likes
            


    return JsonResponse([post.serialize()], safe=False)
