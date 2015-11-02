from django import forms
from blogu.models import Blog
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class BlogForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the blog")
    views = forms.IntegerField(widget=forms.HiddenInput,initial=0)
    slug = forms.CharField(widget=forms.HiddenInput, required=False)
    #content = RichTextField()
    blog_content=RichTextUploadingField()
    likes=forms.IntegerField(widget=forms.HiddenInput,initial=0)
    
    class Meta:
    	model=Blog
    	fields = ('title','blog_content',)
        exclude=('category','written_by','datetime_added',)
    
