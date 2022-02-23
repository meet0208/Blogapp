
from django import forms
from . import models
from django.forms import ModelForm


class ContactForm(ModelForm):
    class Meta:
        model = models.Contact
        fields = '__all__'


class UserdetailForm(ModelForm):
    class Meta:
        model = models.usersave
        fields = '__all__'


class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField()


class UpdateForm(forms.Form):
    # prof = models.usersave.objects.all()
    # for user1 in prof:
    #     if user1_id == user1.user:
            first = forms.CharField(max_length=100)#widget=forms.TextInput(attrs={'value': user1.first}))
            last = forms.CharField(max_length=100)#,widget=forms.TextInput(attrs={'value': user1.last}))
            middle = forms.CharField(max_length=100)#,widget=forms.TextInput(attrs={'value': user1.middle}))
            user = forms.CharField(max_length=100)#,widget=forms.TextInput(attrs={'value': user1.user}))
            email = forms.EmailField()#widget=forms.TextInput(attrs={'value': user1.email}))
            phoneno = forms.CharField(max_length=100)#,widget=forms.TextInput(attrs={'value': user1.phoneno}))


class BlogAddForm(ModelForm):
    class Meta:
        model = models.blogadd
        fields = ['blog_image','blog_title', 'blog_detail']
        