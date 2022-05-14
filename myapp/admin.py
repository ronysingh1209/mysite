from django.contrib import admin
from .models import Contact, Course


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


admin.site.register(Contact, ContactAdmin)
admin.site.register(Course, CourseAdmin)
