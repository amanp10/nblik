from django.contrib import admin
from nblik.models import Category,Blog,Comment,UserProfile,Follow,Tag,Discussion,Discuss

class BlogAdmin (admin.ModelAdmin):
    list_display = ('title','category','written_by','likes','slug')
    prepopulated_fields = { 'slug':('title',)}
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','likes','slug')
    prepopulated_fields = { 'slug':('name',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Blog,BlogAdmin)
admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Discussion)
admin.site.register(Discuss)

# Register your models here.
