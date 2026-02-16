from django.contrib import admin
from .models import Item, Claim, Comment


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'item_type', 'category', 'status', 'posted_by', 'date_reported']
    list_filter = ['item_type', 'category', 'status']
    search_fields = ['title', 'description', 'location']


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['item', 'claimed_by', 'date_claimed', 'is_approved']
    list_filter = ['is_approved']
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'item', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username', 'item__title']
