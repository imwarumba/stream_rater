
from django import forms
from django.contrib.auth.models import User

from stream.models import Streamer, Category, UserProfile, Comment, SubComment

'''
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
         cleaned_data = self.cleaned_data
         url = cleaned_data.get('url')
         if url and not url.startswith('http://'):
             url = 'http://' + url
             cleaned_data['url'] = url
             return cleaned_data

    class Meta:
        model = Page
        exclude = ('category',)

'''


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('website','picture',)#changed


class CommentForm(forms.ModelForm):
    text = forms.TextInput()
    rating = forms.IntegerField(required=True,
                                initial=0,
                                help_text="Rating between 1-5")

    class Meta:
        model = Comment
        fields = ('text', 'rating',)
        exclude = ('streamer', 'user_name',)

    def clean(self):
        cleaned_data = super().clean()
        if not 1 <= cleaned_data.get('rating') <= 5:
            raise forms.ValidationError('Rating between 1 and 5')
        return cleaned_data


class SubCommentForm(forms.ModelForm):
    text = forms.TextInput()

    class Meta:
        model = SubComment
        fields = ('text',)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('text') == "":
            raise forms.ValidationError('Input Empty')
        return cleaned_data