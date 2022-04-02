from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    is_seller = models.BooleanField(null=False, blank=False)
    wallet_hash = models.CharField(max_length=60, null=False, blank=False)

    def __str__(self):
        return f"name: {self.first_name + ' ' + self.last_name} email: {self.email}"


# class EventGeo(models.Model):
#     name = models.CharField(max_length=60, blank=False)
#     location_name = models.CharField(max_length=60, blank=False)
#     address = models.CharField(max_length=60, blank=False)
#     city = models.CharField(max_length=60)
#     state = models.CharField(max_length=60)
#     dateTime = models.DateField(blank=False)
#     lat_long = models.IntegerField(blank=False)  # TODO: Prolly best used with google maps integration


class URL(models.Model):
    link = models.URLField()

    class Meta:
        abstract = True


class Event(models.Model):
    vendor_id = models.ForeignKey(User, on_delete=models.CASCADE)  # If user deleted, delete all associated events
    # geo = models.EmbeddedField(EventGeo, blank=False)
    age_restriction = models.BooleanField(blank=False)
    # images = models.ListField(model_container=URL, default=list)
    tickets_remaining = models.IntegerField()


class Ticket(models.Model):
    # TODO: Determine if the primary key is a combination (hash, id) or just (hash)
    hash = models.CharField(max_length=60, blank=False)  # TODO: Whatever the NFT hash is
    seat = models.CharField(max_length=60)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # TODO: Consider a LazyReferenceField
    price = models.IntegerField(blank=False)
    sale = models.BooleanField(blank=False)
