from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    username = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(primary_key=True, null=False, blank=False)
    is_seller = models.BooleanField(null=False, blank=False)
    avtar_url = models.URLField(max_length=200, null=False, blank=False)
    wallet_addr = models.CharField(max_length=100, null=False, blank=False)
    private_key = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"name: {self.first_name + ' ' + self.last_name} username: {self.username} email: {self.email}"


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
    # If user deleted, delete all associated events
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    # geo = models.EmbeddedField(EventGeo, blank=False)
    age_restriction = models.BooleanField(blank=False)
    # images = models.ListField(model_container=URL, default=list)
    tickets_remaining = models.IntegerField()
    name = models.CharField(max_length=60, default='')
    description = models.CharField(max_length=256, default='')
    location_name = models.CharField(max_length=60, default='')
    address = models.CharField(max_length=60, default='')
    city = models.CharField(max_length=30, default='')
    state = models.CharField(max_length=30, default='')
    date = models.DateField(default='2000-01-01')
    time = models.TimeField(default='00:00:00')


class Ticket(models.Model):
    # TODO: Determine if the primary key is a combination (hash, id) or just (hash)
    # TODO: Whatever the NFT hash is
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=1)
    hash = models.CharField(max_length=60, blank=False)
    seat = models.CharField(max_length=60)
    # TODO: Consider a LazyReferenceField
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(blank=False)
    sale = models.BooleanField(blank=False)
