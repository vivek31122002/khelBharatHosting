from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid, datetime

User = get_user_model()

class Video(models.Model):
    video = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)
    sport = models.CharField(max_length=255, blank=True)
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    location = models.CharField(max_length=255, blank=True)
    sport = models.CharField(max_length=255, blank=True)
    runs_scored = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    profile_type = models.CharField(max_length=255, default='Player')
    rank = models.IntegerField(default=0)
    rank_instance = models.ForeignKey('Rank', on_delete=models.SET_NULL, null=True, blank=True)
    coaches = models.ManyToManyField('self', symmetrical=False, related_name='coached_players', blank=True)
    
class ScoreCard(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)
    sport = models.CharField(max_length=255, blank=True)
    runs_scored = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    profile_type = models.CharField(max_length=255, default='Player')
    rank = models.IntegerField(default=0)
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    no_of_likes = models.IntegerField(default=0)
    
class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    username = models.CharField(max_length=100)
    
class Rank(models.Model):
    rank = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    points = models.IntegerField()
    district = models.CharField(max_length=100)
    
class Rank2(models.Model):
    rank = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    points = models.IntegerField()
    country = models.CharField(max_length=100)
    
    
Profile._signal_saving = False
ScoreCard._signal_saving = False

@receiver(post_save, sender=Profile)
def update_scorecard_and_rank(sender, instance, created, **kwargs):
    if not instance._signal_saving:
        if created:
            ScoreCard.objects.create(
                user=instance,
                location=instance.location,
                sport=instance.sport,
                runs_scored=instance.runs_scored,
                matches_played=instance.matches_played,
                points=instance.points,
                rank=instance.rank,
                profile_type=instance.profile_type
            )
        else:
            scorecard = ScoreCard.objects.get(user=instance)
            scorecard.location = instance.location
            scorecard.sport = instance.sport
            scorecard.runs_scored = instance.runs_scored
            scorecard.matches_played = instance.matches_played
            scorecard.points = instance.points
            scorecard.rank = instance.rank
            scorecard.profile_type = instance.profile_type
            scorecard._signal_saving = True
            scorecard.save(update_fields=['location', 'sport', 'runs_scored', 'matches_played', 'points', 'rank', 'profile_type'])
            scorecard._signal_saving = False

        rank_instance = instance.rank_instance
        if rank_instance is None:
            rank_instance = Rank.objects.create(
                name=instance.user.username,  
                points=instance.points,
                district=instance.location  
            )
            instance.rank_instance = rank_instance
            instance.save(update_fields=['rank_instance'])
        else:
            rank_instance.points = instance.points
            rank_instance.district = instance.location
            rank_instance.save(update_fields=['points', 'district'])

@receiver(post_save, sender=ScoreCard)
def update_profile_from_scorecard(sender, instance, **kwargs):
    if not instance._signal_saving:
        profile = instance.user
        profile.runs_scored = instance.runs_scored
        profile.matches_played = instance.matches_played
        profile.points = instance.points
        profile._signal_saving = True
        profile.save(update_fields=['runs_scored', 'matches_played', 'points'])
        profile._signal_saving = False

        rank_instance = profile.rank_instance
        if rank_instance is None:
            rank_instance = Rank.objects.create(
                name=profile.user.username,  
                points=profile.points,
                district=profile.location  
            )
            profile.rank_instance = rank_instance
            profile.save(update_fields=['rank_instance'])
        else:
            rank_instance.points = profile.points
            rank_instance.district = profile.location
            rank_instance.save(update_fields=['points', 'district'])