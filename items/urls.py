from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/', views.post_item, name='post_item'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('items/', views.item_list, name='item_list'),
    path('item/<int:item_id>/claim/', views.claim_item, name='claim_item'),
    path('item/<int:item_id>/comment/', views.add_comment, name='add_comment'),
    path('item/<int:item_id>/confirm/', views.confirm_receipt, name='confirm_receipt'),
    path('item/<int:item_id>/resolved/', views.mark_resolved, name='mark_resolved'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('claim/<int:claim_id>/approve/', views.approve_claim, name='approve_claim'),
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
]
