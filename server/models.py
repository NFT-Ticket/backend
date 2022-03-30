from djongo import models


# Create your models here.
class User(models.Model):
    _id = models.ObjectIdField(blank=False)
    password = models.CharField(max_length=60, blank=False)
    first_name = models.CharField(max_length=60, blank=False)
    last_name = models.CharField(max_length=60, blank=False)
    email = models.EmailField(blank=False)
    is_seller = models.BooleanField(blank=False)
    wallet_hash = models.CharField(max_length=60, blank=False)


class EventGeo(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=60, blank=False)
    location_name = models.CharField(max_length=60, blank=False)
    address = models.CharField(max_length=60, blank=False)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    dateTime = models.DateField(blank=False)
    lat_long = models.IntegerField()  # TODO: Prolly best used with google maps integration


class URL(models.Model):
   link = models.URLField()
   class Meta:
        abstract = True

class Event(models.Model):
    _id = models.ObjectIdField()
    vendor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    geo = models.EmbeddedField(EventGeo, blank=False)
    age_restriction = models.BooleanField(blank=False)
    images = models.ArrayField(model_container=URL, default=list)
    tickets_remaining = models.IntegerField()

class Ticket(models.Model):
    # TODO: Determine if the primary key is a combination (hash, id) or just (hash)
    _id = models.ObjectIdField()
    hash = models.CharField(max_length=60, blank=False)  # TODO: Whatever the NFT hash is
    seat = models.CharField(max_length=60)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # TODO: Consider a LazyReferenceField
    price = models.IntegerField(blank=False)
    sale = models.BooleanField(blank=False)
