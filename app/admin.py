from django.contrib import admin
from app.models import Video, Profile, CustomUser, Post, LikePost, Rank, ScoreCard

# Register your models here.
class RankAdmin(admin.ModelAdmin):
    list_display = ('rank', 'name', 'points', 'district')
    
class VideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'title', 'description', 'uploaded_at')
    
class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'title', 'description', 'uploaded_at')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'sport', 'runs_scored', 'matches_played', 'points', 'rank', 'profile_type', 'bio', 'profileimg')
    
class ScoreCardAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'location', 'sport', 'runs_scored', 'matches_played', 'points', 'rank', 'profile_type')

    def get_username(self, obj):
        return obj.user.user.username

    get_username.short_description = 'User'
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'sport')
    
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'caption', 'created_at', 'no_of_likes')
    list_filter = ('user', 'created_at')
    search_fields = ('user', 'caption')
    readonly_fields = ('id', 'created_at')
    
admin.site.register(Video, VideoAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ScoreCard, ScoreCardAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost)
admin.site.register(Rank, RankAdmin)
