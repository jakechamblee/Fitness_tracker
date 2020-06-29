from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Voter
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class IndexView(ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        """
        Returns the last five published questions, but not those set to be published in the future.
        Excludes questions with no choices.
        """
        return Question.objects.filter(pub_date__lte=timezone.now(),
                                       choice__isnull=False).distinct().order_by('-pub_date')[:5]


class PollDetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes unpublished questions (questions for the future) to prevent premature user access.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if Voter.objects.filter(poll_id=question_id, user_id=request.user.id).exists():
        return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You have already voted on this poll.",
            })
    else:
        try:
            # choice_set is getting the choices for Question as a queryset. It does this as the Choice models have a
            # foreign key which relates to Question, so choice_set automatically is created to reference that queryset
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # creating a voter model for the question and voter
            v = Voter(user=request.user, poll=question)
            v.save()
            # Always return an HttpResponseRedirect after successfully dealing with POST data.
            # This prevents data from being posted twice if a user hits the Back button.
            return HttpResponseRedirect(reverse('polls-results', args=(question.id,)))
