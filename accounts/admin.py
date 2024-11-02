from django.contrib import admin
from customer.models import Contacts
from accounts.models import User

# Register your models here.
class ContactUser(admin.StackedInline):
    model = Contacts

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username']
    inlines = [ContactUser]

admin.site.register(User, UserAdmin)