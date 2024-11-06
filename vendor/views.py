from django.http import JsonResponse
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
        'vendor' : vendor,
        'product_count': vendor.product_vendor.count()
    })


def view_products(request):
    try:
        products = Product.objects.filter(vendor = request.user)
        return render(request, 'vendor/products.html', {
            'products' : products
        })
    except Exception as e:
        print(e)
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
                    
            return redirect('vendor:products')  # Redirect to desired view
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


def add_category(request):
    form = CategoryForm(request.POST, request.FILES)
    if form.is_valid():
        category = form.save()
        return JsonResponse({
            'id': category.uid,
            'name': category.name
        }, status=200)
    
    else:
        return JsonResponse({
            'error' : 'Error adding category.'
        }, status = 400)
    return redirect('vendor:add_category')


def add_color_variant(request):
    form = ColorVariantForm(request.POST)
    if form.is_valid():
        color_name = form['name'].value()
        color = ColorVariant.objects.create(name = color_name.lower())
        
        return JsonResponse({
            'id' : color.uid,
            'name' : color.name
        },status = 200)
    else:
        return JsonResponse({
            'error' : "Error adding color."
        }, status = 400)
    

def add_size_variant(request):
    form = SizeVariantForm(request.POST)
    if form.is_valid():
        size_name = form['name'].value()
        size = SizeVariant.objects.create(name = size_name.upper())

        return JsonResponse({
            'id' : size.uid,
            'name' : size.name
        }, status = 200)
    else:
        return JsonResponse({
            'error' : "Error addig size."
        }, status = 400)