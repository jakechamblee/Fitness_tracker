# from datetime import datetime
# from django import forms
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
#
# from .models import ExerciseInstance, Exercise
#
#
# class ExerciseForm(forms.ModelForm):
#     # django automatically cleans data and stores it in the cleaned_data attribute
#     # django's form system automatically looks for any method which starts with 'clean_' and ends with the name of
#     # a field. It then calls those methods during validation.
#     def clean_date_performed(self):
#         data = self.cleaned_data['date_performed']
#
#         if data > datetime.date.today():
#             raise ValidationError('Invalid date - date is in the future.')
#
#         return data
#
#     class Meta:
#         model = ExerciseInstance
#         fields = ['name', 'date_performed', 'sets', 'reps', 'weight', 'user']
#         # labels = {'name': 'exercise'}

