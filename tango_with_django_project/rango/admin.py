from django.contrib import admin
from rango.models import Category, Page, UserProfile


class PageInline(admin.TabularInline):
    model = Page
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['name']
        }),
        ('Information', {
            'fields': ['views', 'likes']
        }),
    ]
    list_display = ('name', 'views', 'likes')
    inlines = [PageInline]
    list_filter = ['name']


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['title']
        }),
        ('Information', {
            'fields': ['url', 'views', 'category']
        }),
    ]
    list_display = ('title', 'category', 'url', 'views')
    search_fields = ['category', 'title']
    list_filter = ['category']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
