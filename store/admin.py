from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User

# Register the  models.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

# Mix profile info with user info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend the user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "lasr_name", "email"]
    inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)
