from .models import Post
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, TimeInput

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'datetime', 'author']

        widgets = {
                'title' : TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Заголовок'
                }),
                'text' : Textarea(attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Введите свою запись'                    
                }), 
                'datetime' : DateTimeInput(attrs={
                    'class' : 'form-control',
                    'placeholder' : 'дата и время'                    
                }), 
                'author' : TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Автор'                   
                }),                                                        
        }