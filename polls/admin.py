from django.contrib import admin
from .models import Question, Choice

# Register your models here.
"""
OLD
class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

# admin.site.register(Choice)
"""


class ChoiceInline(admin.TabularInline):
    # admin.StackedInline instead of admin.TabularInline
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    # Adds a “Filter” sidebar
    list_filter = ['pub_date']

    search_fields = ['question_text', 'pub_date']


admin.site.register(Question, QuestionAdmin)
