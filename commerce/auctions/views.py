from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings":listings,
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def createListing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startBid = float(request.POST["startBid"])
        imageURL = request.POST["imageURL"]

        ownerId = int(request.POST["ownerId"])
        owner = User.objects.get(id=ownerId)

        categoryId = request.POST["categoryId"]
        
        if categoryId != "None":
            category = Category.objects.get(id=int(categoryId))
            item = Listing(title=title, description=description, startBid=startBid,imageURL=imageURL,owner = owner, category=category)
            item.save()
        else:
            item = Listing(title=title, description=description, startBid=startBid,imageURL=imageURL,owner = owner)
            item.save()
        
        return HttpResponseRedirect(reverse("index"))
            
    categories = Category.objects.all()

    return render(request, "auctions/createListing.html", {
        "categories" : categories,
    })

def viewListing(request, listingId):
    item = Listing.objects.get(id=listingId)
    return render(request, "auctions/viewListing.html", {
        "item": item,
    })

def makeBid(request, listingId):
    listing = Listing.objects.get(id=int(listingId))

    bidValue = float(request.POST["bid"])

    bidsCount = listing.bids.all().count()

    if bidsCount == 0 and bidValue >= listing.startBid or bidsCount != 0 and bidValue > listing.bids.last().value:
        bidderId = int(request.POST["bidderId"])
        bidder = User.objects.get(id=bidderId)

        bid = Bid(bidder=bidder, item=listing, value=bidValue)
        bid.save()
        listing.interestedUsers.add(bidder)
    elif bidsCount == 0 and bidValue < listing.startBid:
        return render(request, "auctions/viewListing.html", {
                "message": "Your bid value should be equal or greater than the current one.",
                "item" : listing,
            })
    elif bidsCount != 0 and bidValue <= listing.bids.last().value:
        return render(request, "auctions/viewListing.html", {
                "message": "Your bid value should be greater than the current one.",
                "item" : listing,
            })

    return HttpResponseRedirect(reverse("viewListing", args=[listingId]))

def addWatchlist(request, listingId):
    interestedUserId = int(request.POST["interestedUserId"])

    interestedUser = User.objects.get(id=interestedUserId)
    listing = Listing.objects.get(id=int(listingId))

    listing.interestedUsers.add(interestedUser)


    return HttpResponseRedirect(reverse("viewListing", args=[listingId]))

def removeWatchlist(request, listingId):
    interestedUserId = int(request.POST["interestedUserId"])

    interestedUser = User.objects.get(id=interestedUserId)
    listing = Listing.objects.get(id=int(listingId))

    listing.interestedUsers.remove(interestedUser)

    return HttpResponseRedirect(reverse("viewListing", args=[listingId]))

def makeComment(request, listingId):
    commenterId = int(request.POST["commenterId"])
    content = request.POST["content"]

    commenter = User.objects.get(id=commenterId)
    listing = Listing.objects.get(id=int(listingId))

    comment = Comment(commenter=commenter, item=listing, content=content)
    print(comment)
    comment.save()
    return HttpResponseRedirect(reverse("viewListing", args=[listingId]))

def viewWatchlist(request):
    return render(request, "auctions/viewWatchlist.html")

def viewCategories(request):
    listCategories = Category.objects.all()
    return render(request, "auctions/viewCategories.html", {
        "listCategories" : listCategories,
    })

def viewCategory(request, categoryId):
    category = Category.objects.get(id=int(categoryId))
    categoryListings = category.listings.all()

    return render(request, "auctions/viewCategory.html", {
        "categoryName" : category.categoryName,
        "categoryListings" : categoryListings,
    })

def desactiveListing(request):
    listingId = int(request.POST["listingId"])
    listing = Listing.objects.get(id=listingId)

    listing.isActive = False
    listing.save()

    return HttpResponseRedirect(reverse("viewListing", args=[listingId]))