from django.contrib import admin
from catalog.models import CustomerUser
from .models import Category, Application

admin.site.register(CustomerUser)

@admin.register(Category)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'status', 'created_at']