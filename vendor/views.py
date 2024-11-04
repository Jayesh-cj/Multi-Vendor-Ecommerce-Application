from django.shortcuts import redirect, render
from django import forms

from accounts.models import User
from products.models import ProductImages

from vendor.froms import *

# Create your views here.
def homepage(request):
    try:
        vendor = User.objects.get(uid = request.user.uid)
    except Exception as e:
        print(e)
    return render(request,'vendor/homepage.html',{
        'vendor' : vendor
    })


def view_products(request):
    return render(request, 'vendor/products.html')


def add_product(request):
    ImageFormSet = forms.modelformset_factory(ProductImages, form=ProductImagesForm, extra=1, can_delete=True)
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImages.objects.none())
        
        if product_form.is_valid() and image_formset.is_valid():
            # Save the product instance without committing so we can set vendor and m2m fields
            product = product_form.save(commit=False)
            product.vendor = request.user
            product.save()  # Save product to set up m2m relationships

            # Set only the selected color and size variants
            product.colors.set(product_form.cleaned_data['colors'])
            product.sizes.set(product_form.cleaned_data['sizes'])

            # Process each image in the formset
            for form in image_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    image = form.save(commit=False)
                    image.product = product
                    image.save()
                    
            return redirect('product_list')  # Redirect to desired view
    else:
        product_form = ProductForm()
        image_formset = ImageFormSet(queryset=ProductImages.objects.none())

    return render(request, 'vendor/add_product.html', {
        'category_form' : CategoryForm(),
        'color_form' : ColorVariantForm(),
        'size_form' : SizeVariantForm(),
        'product_form': product_form,
        'image_formset': image_formset,
    })
