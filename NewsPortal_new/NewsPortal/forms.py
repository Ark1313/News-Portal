from django import forms
from .models import Post, Author
from django.core.exceptions import ValidationError
from django.http import HttpRequest



class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = '__all__'




class PostCreateForm(forms.ModelForm):

    p_type = forms.CharField(
        widget=forms.HiddenInput,
    )


    class Meta:
        model = Post

        fields = ['p_name', 'p_post', 'p_category', 'p_author', 'p_type']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("p_post")
        name = cleaned_data.get("p_name")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data

