from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('electronics', 'Electronics'),
    ('books', 'Books'),
    ('clothing', 'Clothing'),
    ('accessories', 'Accessories'),
    ('id_cards', 'ID Cards'),
    ('keys', 'Keys'),
    ('bags', 'Bags'),
    ('other', 'Other'),
]

ITEM_TYPE_CHOICES = [
    ('lost', 'Lost'),
    ('found', 'Found'),
]

STATUS_CHOICES = [
    ('open', 'Open'),
    ('claimed', 'Claimed'),
    ('resolved', 'Resolved'),
]


class Item(models.Model):
    """Represents a lost or found item posted by a user."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    item_type = models.CharField(max_length=5, choices=ITEM_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    location = models.CharField(max_length=200)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_item = models.DateField(help_text='Date when item was lost or found')
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')

    class Meta:
        ordering = ['-date_reported']

    def __str__(self):
        return f"[{self.get_item_type_display()}] {self.title}"


class Claim(models.Model):
    """A claim request made by a user on an item."""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    message = models.TextField(help_text='Describe why you think this is yours')
    date_claimed = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_claimed']

    def __str__(self):
        return f"Claim by {self.claimed_by.username} on {self.item.title}"
