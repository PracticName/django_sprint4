from django.contrib import admin

from .models import Category, Location, Post

admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'created_at',
        'is_published',
        'author',
        'location',
        'category',
    )
    list_editable = (
        'pub_date',
        'author',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'is_published',
    )
    list_editable = (
        'slug',
        'is_published'
    )
    search_fields = (
        'title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
