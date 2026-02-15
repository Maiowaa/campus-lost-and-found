from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Item, Claim
from .forms import RegisterForm, ItemForm, ClaimForm, SearchForm


def home(request):
    """Landing page showing 6 most recent items."""
    recent_items = Item.objects.filter(status='open')[:6]
    lost_count = Item.objects.filter(item_type='lost').count()
    found_count = Item.objects.filter(item_type='found').count()
    resolved_count = Item.objects.filter(status='resolved').count()
    return render(request, 'items/home.html', {
        'recent_items': recent_items,
        'lost_count': lost_count,
        'found_count': found_count,
        'resolved_count': resolved_count,
    })


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'items/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'items/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def post_item(request):
    """Create a new lost or found item listing."""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by = request.user
            item.save()
            messages.success(request, 'Item posted successfully!')
            return redirect('item_detail', item_id=item.id)
    else:
        form = ItemForm()
    return render(request, 'items/post_item.html', {'form': form})


def item_detail(request, item_id):
    """Show full details of an item with claim form."""
    item = get_object_or_404(Item, id=item_id)
    claims = item.claims.all()
    claim_form = ClaimForm()

    # Check if current user already claimed this item
    user_has_claimed = False
    if request.user.is_authenticated:
        user_has_claimed = claims.filter(claimed_by=request.user).exists()

    return render(request, 'items/item_detail.html', {
        'item': item,
        'claims': claims,
        'claim_form': claim_form,
        'user_has_claimed': user_has_claimed,
    })


def item_list(request):
    """Search and filter items."""
    form = SearchForm(request.GET)
    items = Item.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        item_type = form.cleaned_data.get('item_type')

        if query:
            items = items.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
            )
        if category:
            items = items.filter(category=category)
        if item_type:
            items = items.filter(item_type=item_type)

    return render(request, 'items/item_list.html', {'items': items, 'form': form})


@login_required
def claim_item(request, item_id):
    """Submit a claim on an item."""
    item = get_object_or_404(Item, id=item_id)

    if request.user == item.posted_by:
        messages.warning(request, "You can't claim your own item.")
        return redirect('item_detail', item_id=item.id)

    if Claim.objects.filter(item=item, claimed_by=request.user).exists():
        messages.info(request, 'You have already claimed this item.')
        return redirect('item_detail', item_id=item.id)

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimed_by = request.user
            claim.save()
            item.status = 'claimed'
            item.save()
            messages.success(request, 'Claim submitted successfully!')
    return redirect('item_detail', item_id=item.id)


@login_required
def dashboard(request):
    """Show user's posted items and claims."""
    my_items = Item.objects.filter(posted_by=request.user)
    my_claims = Claim.objects.filter(claimed_by=request.user)
    # Claims on user's items (incoming claims to review)
    incoming_claims = Claim.objects.filter(item__posted_by=request.user)
    return render(request, 'items/dashboard.html', {
        'my_items': my_items,
        'my_claims': my_claims,
        'incoming_claims': incoming_claims,
    })


@login_required
def approve_claim(request, claim_id):
    """Approve a claim — only the item poster can approve."""
    claim = get_object_or_404(Claim, id=claim_id)

    if request.user != claim.item.posted_by:
        messages.error(request, 'You are not authorized to approve this claim.')
        return redirect('dashboard')

    if request.method == 'POST':
        claim.is_approved = True
        claim.save()
        claim.item.status = 'resolved'
        claim.item.save()
        messages.success(request, f'Claim by {claim.claimed_by.username} approved!')
    return redirect('dashboard')


@login_required
def delete_item(request, item_id):
    """Delete an item — only the poster can delete."""
    item = get_object_or_404(Item, id=item_id)

    if request.user != item.posted_by:
        messages.error(request, 'You are not authorized to delete this item.')
        return redirect('dashboard')

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully.')
    return redirect('dashboard')
