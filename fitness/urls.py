from django.urls import include, path
from . import views
from .views import ExerciseInstanceListView, ExerciseInstanceCreateView, ExerciseInstanceUpdateView

urlpatterns = [
    path('', ExerciseInstanceListView.as_view(), name='fitness-home'),
    path('fitness_create_form/', ExerciseInstanceCreateView.as_view(), name='fitness-create'),
    path('progress/<str:exercise_name>/', views.exerciseinstancesgraph, name='fitness-progress'),
    path('update/<int:pk>/', ExerciseInstanceUpdateView.as_view(), name='fitness-update'),
]