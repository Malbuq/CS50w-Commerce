from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.categoryName}"


class Listing(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length = 500, blank=True)
    imageURL = models.CharField(max_length = 1000, blank=True)
    startBid = models.FloatField()
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "listings")
    category = models.ForeignKey(Category, blank=True, null=True, on_delete = models.CASCADE, related_name = "listings")
    interestedUsers = models.ManyToManyField(User, blank=True,  null = True, related_name = "watchlist")

    def __str__(self):
        return f"({self.title}) was listed by {self.owner} with starting bid of $ {self.startBid}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name = "commentaries")
    item = models.ForeignKey(Listing, on_delete = models.DO_NOTHING, related_name = "commentaries")
    content = models.TextField()
    
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment made by {self.commenter} at {self.date}, saying: {self.content}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name = "bids")
    item = models.ForeignKey(Listing, on_delete = models.DO_NOTHING, related_name = "bids")
    value = models.FloatField()

    def __str__(self):
        return f"Bid made by {self.bidder} with the value of: $ {(self.value)} in the item {self.item}"


