from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name="index"),
    path('profile/', views.profile_page, name="profile_page"),
    path('profile-page/<str:pk>', views.profile, name="profile"),
    path('schemes/', views.schemes, name="schemes"),
    path('loans/', views.loans, name="loans"),
    path('change-profile-type/<str:pk>', views.change_profile_type, name="change_profile_type"),
    path('edit-player-scorecard/', views.edit_player_scorecard, name="edit_player_scorecard"),
    path('update-scorecard/<str:pk>', views.update_scorecard, name="update_scorecard"),
    path('test', views.test, name="test"),
    path('upload-video/', views.upload_video, name="upload_video"),
    path('upload-post/', views.upload_post, name="upload_post"),
    path('like-post/', views.like_post, name="like_post"),
    path('content/', views.content, name="content"),
    path('social', views.social, name="social"),
    path('rank/', views.rank, name="rank"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.logout, name="logout"),
    path('shopcricket/', views.shopcricket, name="shopcricket"),
    path('cricket/', views.cricket, name="cricket"),
    path('cricket/shopcricket', views.shopcricket, name="shopcricket"),
    # path('sos', views.sos, name="sos"),
    path('coaches', views.coaches, name="coaches"),
    path('sponsers', views.sponsers, name="sponsers"),
    path('women-safety-page', views.women_safety, name="women_safety"),
    path('funds-page', views.funds, name="funds"),
    path('sports-politics-page', views.sports_politics, name="sports_politics"),
    path('player-list/', views.player_list, name='player_list'),
    path('add-player/', views.add_player, name='add_player'),
    path('players-and-coaches/', views.players_and_coaches, name='players_and_coaches'),
]