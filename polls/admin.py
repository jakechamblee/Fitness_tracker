from django.contrib import admin
from .models import Question, Choice


# Creating a class for adding Choice inline to a model's admin page
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    # Adding inline choices for Choice to the admin page of Question
    inlines = [ChoiceInline]

    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # creates a filter sidebar for filtering by 'pub_date'
    list_filter = ['pub_date']
    # creates a search field for searching 'question_text'. Can search any number of fields, but search will be slower.
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
