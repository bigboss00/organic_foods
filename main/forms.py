from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Product, Blog, Review


class CreateProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Product
        exclude = ('user', )

    def save(self, commit=True):
        product = super().save(commit=False)
        product.user = self.request.user
        product.save()
        return product


class CreateCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Category
        exclude = ('user', )

    def save(self, commit=True):
        category = super().save(commit=False)
        category.user = self.request.user
        category.save()
        return category


class CreateBlogForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Blog
        exclude = ('user', )

    def save(self, commit=True):
        blog = super().save(commit=False)
        blog.user = self.request.user
        blog.save()
        return blog

    
class CreateReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Review
        exclude = ('user', )

    def save(self, commit=True):
        review = super().save(commit=False)
        review.user = self.request.user
        review.save()
        return review


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user', )


class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('user', )


class UpdateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('user', )


class UpdateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user', )


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'name': 'username',
            'type': 'text',
            'class': 'register__input',
            'placeholder': 'Username'
        })
        self.fields["email"].widget.attrs.update({
            'name': 'email',
            'type': 'email',
            'class': 'register__input',
            'placeholder': 'Email'
        })
        self.fields["password1"].widget.attrs.update({
            'name': 'email',
            'type': 'password',
            'class': 'register__input',
            'placeholder': 'Password'
        })
        self.fields["password2"].widget.attrs.update({
            'name': 'email',
            'type': 'password',
            'class': 'register__input',
            'placeholder': 'Password confirm'
        })

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
