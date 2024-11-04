from django import forms
from products.models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : "Enter category",
                'required' : True
            }),
            'image' : forms.FileInput(attrs={
                'class' : 'form-control'
            })
        }

class ColorVariantForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : "Enter the color",
                'required' : True
            })
        }

class SizeVariantForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : "Enter new size (e.g., S, M, L)",
                'required' : True
            })
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['uid', 'vendor', 'slug']

        widgets = {
            'category' : forms.Select(attrs={
                'class' : 'form-control',
            }),
            'colors' : forms.SelectMultiple(attrs = {
                    'class' : 'form-control',
                },
                choices=ColorVariant.objects.all(),
            ),
            'sizes' : forms.SelectMultiple(attrs={
                'class' : 'form-control',
                },
                choices=SizeVariant.objects.all()
            ),
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Product Name',
                'required' : True
            }),
            'description' : forms.Textarea(attrs={
                'class' : 'form-control',
                'rows' : 5,
                'placeholder' : 'Product Description...'
            }),
            'price' : forms.NumberInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Product Price'
            }),
            'stock' : forms.NumberInput(attrs={
                'class' : 'form-control'
            })
        }


class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image']
        widgets = {
            'image' : forms.FileInput(attrs={
                'class' : 'form-control'
            })
        }