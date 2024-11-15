from django.db import models
from django.utils.text import slugify
from base.models import BaseModel
from accounts.models import User

# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='category/')
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **Kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
            self.slug = f"{self.slug}-{str(self.uid)[:5]}"
        return super(Category, self).save(*args, **Kwargs)
    
    class Meta:
        ordering = ['name']
        

class ColorVariant(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        ordering = ['name']

class SizeVariant(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
    

class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_vendor')
    colors = models.ManyToManyField(ColorVariant, blank=True)
    sizes = models.ManyToManyField(SizeVariant, blank=True)
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    stock = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
            if Product.objects.filter(slug = self.slug).exists():
                self.slug = f"{self.slug}-{str(self.uid)[:5]}"
        return super(Product, self).save(*args, **kwargs)  
          

class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.FileField(upload_to='product/')

    def __str__(self) -> str:
        return self.product.name