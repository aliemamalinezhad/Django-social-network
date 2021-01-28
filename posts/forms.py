from django import forms
from .models import Post, Comment


class AddPostsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }
        error_messages = {
            'body': {
                'required': 'این فیلد اجباری است .'
            }
        }

class AddReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)