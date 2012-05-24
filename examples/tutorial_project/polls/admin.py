from django.contrib import admin

from .models import Poll, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    readonly_fields = ('votes',)
    extra = 3


class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'pub_date', 'was_published_recently')
    search_fields = ['question']
    date_hierarchy = 'pub_date'

    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    inlines = [ChoiceInline]


admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)


