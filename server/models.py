from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    username = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(primary_key=True, null=False, blank=False)
    is_seller = models.BooleanField(null=False, blank=False)
    avtar_url = models.URLField(max_length=200, null=False, blank=False)
    wallet_addr = models.CharField(max_length=100, blank=True)
    private_key = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"name: {self.first_name + ' ' + self.last_name} username: {self.username} email: {self.email}"


class Event(models.Model):
    # If user deleted, delete all associated events
    # foreign_key = pk of User creating event
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_quantity = models.PositiveIntegerField(null=False, blank=False)
    tickets_remaining = models.PositiveIntegerField(blank=True)
    # NFT asset id associated with Event ticket
    # Remember that each event will be associated with one NFT id
    # Storing nft_id here minimizes data redundancy in Tickets table
    ticket_nft_id = models.CharField(max_length=60, blank=True)
    title = models.CharField(
        max_length=64, default='EVENT TITLE', null=False, blank=False)
    description = models.TextField(
        default='EVENT DESCRIPTION', null=False, blank=False)
    # JSON stored as textfield
    images = models.JSONField(default=dict, null=False, blank=False)
    street_address = models.CharField(
        max_length=60, null=False, blank=False, default="300 Circle Rd")
    city = models.CharField(max_length=32, null=False,
                            blank=False, default="Stony Brook")
    zipcode = models.CharField(
        max_length=5, null=False, blank=False, default="11790")
    state = models.CharField(max_length=30, null=False,
                             blank=False, default="New York")
    date = models.DateField(null=False, blank=False, default="2022-05-20")
    time = models.TimeField(null=False, blank=False, default="00:00:00")


class Ticket(models.Model):
    # IF event is deleted, delete all associated tickets
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # NFT asset id associated with ticket
    nft_id = models.CharField(max_length=60, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_expired = models.BooleanField(null=False, blank=False)
    on_sale = models.BooleanField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
