# forms.py
from django import forms
from .models import Video
from .models import Profile

class AddPlayerForm(forms.Form):
    player = forms.ModelChoiceField(queryset=Profile.objects.filter(profile_type='Player'))
    
    def __init__(self, *args, **kwargs):
        super(AddPlayerForm, self).__init__(*args, **kwargs)
        self.fields['player'].label_from_instance = lambda obj: obj.user.username
    
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video', 'title', 'description']
