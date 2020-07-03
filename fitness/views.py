from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.messages import constants
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Exercise, ExerciseInstance
from django.contrib.auth.models import User
from .graphs import fitness_graph


class ExerciseInstanceListView(LoginRequiredMixin, ListView):
    model = ExerciseInstance
    template_name = 'fitness/fitness_home_table.html'
    context_object_name = 'exercise_instances'
    paginate_by = 15

    def get_queryset(self):
        current_user = self.request.user
        return ExerciseInstance.objects.filter(user=current_user).order_by('-date_performed')

    def get_context_data(self, *, object_list=None, **kwargs):
        # Calling the base implementation to get a context
        context = super().get_context_data(**kwargs)
        # Adding exercise_names to the context in addition to the listview queryset exercise_instances
        context['exercise_names'] = Exercise.objects.all()
        return context


class ExerciseInstanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExerciseInstance
    fields = ['name', 'sets', 'reps', 'weight']
    template_name = 'fitness/fitness_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # get_object looks for a pk or slug in the url by default
        instance = self.get_object()
        if self.request.user == instance.user:
            return True
        else:
            return False


def exerciseinstancesgraph(request, **kwargs):
    """ Gets the ExerciseInstance data filtered for the currently logged in user, and
    for the particular exercise passed when the user clicks on an Exercise link
    """
    # Gets the current user's data as a queryset
    current_user_id = request.user.id
    all_user_data = ExerciseInstance.objects.filter(user_id=current_user_id)

    exercise_name_ids = {ex.name: ex.id for ex in Exercise.objects.all()}

    # Gets the Exercise model with the name passed in the captured URL via kwargs
    ex_name = get_object_or_404(Exercise, name=kwargs.get('exercise_name'))
    exercise_id = exercise_name_ids[ex_name.name]

    # Filters the user's data for only instances of the exercise name which was clicked
    fitness_queryset = all_user_data.filter(name_id=exercise_id)

    graph = fitness_graph(fitness_queryset, ex_name)
    # IMPROVEMENT: do not add names to exercise_names if there is no data for that exercise
    exercise_names = Exercise.objects.all()

    context = {'graph': graph, 'exercise_names': exercise_names, 'ex_name': ex_name}
    return render(request, template_name='fitness/progress.html', context=context)


class ExerciseInstanceCreateView(LoginRequiredMixin, CreateView):
    model = ExerciseInstance
    fields = ['name', 'sets', 'reps', 'weight']
    template_name = 'fitness/fitness_create_form.html'

    def get_success_url(self):
        return reverse('fitness-create')

    def form_valid(self, form):
        # overriding form_valid() to set the author to the user creating the post
        form.instance.user = self.request.user
        return super().form_valid(form)
