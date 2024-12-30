from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth, User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse
from .forms import VideoForm, AddPlayerForm
from app.models import Video, Profile, CustomUser, Post, LikePost, Rank, Rank2,ScoreCard

from twilio.rest import Client


@login_required(login_url='signin')
def profile_page(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        
        posts = Post.objects.all().filter(user=user_object)
        return render(request, 'profile.html', {"user_profile" : user_profile, "posts" : posts})
    except:
        return redirect('signin')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = get_object_or_404(User, username=pk)
    user_profile = Profile.objects.get(user=user_object)
    no_of_posts = Post.objects.filter(user=user_object).count()
    
    context = {
        "user_profile": user_profile,
        "user_object": user_object,
        "no_of_posts": no_of_posts,
    }
    
    return render(request, 'user_profile.html', context=context)

@login_required(login_url='signin')
def change_profile_type(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    
    if user_profile.profile_type == 'Player':
        user_profile.profile_type = 'Coach'
    elif user_profile.profile_type == 'Coach':
        user_profile.profile_type = 'Player'
    
    user_profile.save()
    
    return redirect('profile_page')
  
@login_required(login_url='signin')              
def edit_player_scorecard(request):
    all_scorecards = ScoreCard.objects.filter(profile_type='Player')
    context = {
        "all_scorecards": all_scorecards,
    }
    
    return render(request, 'edit_player_scorecard.html', context=context)

def update_scorecard(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    scorecard = ScoreCard.objects.get(user=user_profile)
    
    if request.method == 'POST':
        scorecard.runs_scored = request.POST['runs_scored']
        scorecard.matches_played = request.POST['matches_played']
        scorecard.points = request.POST['points']
        
        scorecard.save()
        messages.success(request, 'Scorecard updated successfully')
        return redirect('edit_player_scorecard')
    else:
        messages.error(request, 'Error updating scorecard')
        return redirect('edit_player_scorecard')

@login_required(login_url='signin')
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'upload.html', {'form': form, 'success': True})
        else:
            return render(request, 'upload.html', {'form': form, 'success': False})
    else:
        form = VideoForm()
    return render(request, 'upload.html', {'form': form})

@login_required(login_url='signin')
def upload_post(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES['image']
        caption = request.POST['caption']
        
        user_object = User.objects.get(username=user)
        new_post = Post.objects.create(image=image, caption=caption, user=user_object)
        new_post.save()
        return redirect('profile_page')
    else:
        return render(request, 'upload_post.html')

@login_required(login_url='signin')
def content(request):   
    videos = Video.objects.all()
    return render(request, 'content.html', {'videos': videos})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        location = request.POST.get('location', '')
        sport = request.POST.get('sport', '')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            custom_user = CustomUser.objects.create(user=user, location=location, sport=sport)
            user = authenticate(username=username, password=password)
            if user is not None:
                custom_user.save()
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, location=location, sport=sport)
                new_profile.save()
                return redirect('signin')
            else:
                return render(request, 'signup.html', {'error': 'Authentication failed'})
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profile_page')
        else:
            return render(request,'signin.html', {'error': 'Authentication failed'})
    else:
        return render(request,'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')
    
@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('profile_page')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('profile_page')
    
    
@login_required(login_url='signin')
def social(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    all_posts = Post.objects.all()
    
    return render(request,'social.html', {'all_posts' : all_posts, "user_profile" : user_profile})

# custom function
def update_ranks():
    all_ranks = Rank.objects.all().order_by('-points')
    for index, rank in enumerate(all_ranks):
        rank.rank = index + 1
        rank.save()
        
    all_ranks2 = Rank2.objects.all().order_by('-points')
    for index, rank in enumerate(all_ranks2):
        rank.rank = index + 1
        rank.save()
        
@login_required(login_url='signin')
def rank(request):
    update_ranks()
    districts = Rank.objects.values_list('district', flat=True).distinct()
    selected_place = request.GET.get('district', 'all-districts')
    search_query = request.GET.get('search', '')

    if selected_place == "all-districts":
        ranks = Rank.objects.all().order_by('rank')
    elif selected_place == "all-countries":
        ranks = Rank2.objects.all().order_by('rank')
    else:
        ranks = Rank.objects.filter(district=selected_place).order_by('rank')
    
    if search_query:
        ranks = ranks.filter(
            Q(name__icontains=search_query) |
            Q(rank__icontains=search_query) |
            Q(points__icontains=search_query) |
            Q(district__icontains=search_query)
        )

    context = {
        'districts': districts,
        'selected_place': selected_place,
        'ranks': ranks,
        'search_query': search_query,
    }
    return render(request, 'rank.html', context)


def player_list(request):
    players = Profile.objects.filter(profile_type='Player')
    return render(request, 'player_list.html', {'players': players})

@login_required
def add_player(request):
    if request.method == 'POST':
        form = AddPlayerForm(request.POST)
        if form.is_valid():
            player = form.cleaned_data['player']
            coach = Profile.objects.get(user=request.user)
            coach.coaches.add(player)
            coach.save()
            # return redirect('player_list')
    else:
        form = AddPlayerForm()
    return render(request, 'add_player.html', {'form': form})

def players_and_coaches(request):
    players = Profile.objects.filter(profile_type='Player')
    context = {'players': players}
    return render(request, 'players_and_coaches.html', context)

def test(request):
    context = {'name': 'test', 'message' : 'Welcome'}
    return render(request, 'test.html', context)

def home(request):
    return render(request, 'try.html')

def schemes(request):
    return render(request,'schemes.html')

def loans(request):
    return render(request, 'loans.html')

def cricket(request):
    return render(request, 'cricket.html')

def shopcricket(request):
    return render(request,'shopcricket.html')

# def sos(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone')
#         sos_message = request.POST.get('message')

#         account_sid = 'sid'
#         auth_token = 'token'
#         client = Client(account_sid, auth_token)

#         message = client.messages.create(
#             from_='+12202054101',
#             body=sos_message,
#             to=phone_number
#         )
#         print(message.sid)
#         return HttpResponse('SOS message sent successfully.')
#     else:
#         return render(request,'sos.html')

def coaches(request):
    return render(request, 'coaches.html')

def sponsers(request):
    return render(request,'sponsers.html')

def women_safety(request):
    return render(request, 'women.html')

def funds(request):
    return render(request, 'funds.html')

def sports_politics(request):
    return render(request,'politics.html')