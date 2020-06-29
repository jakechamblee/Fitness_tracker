import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


# django will look for subclasses of the TestCase class in tests.py
class QuestionModelTests(TestCase):

    # django will then look for methods which begin with the name "test" (test methods)
    def test_was_published_recently_with_old_question(self):
        """
        should return False for questions with a publication date older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=2)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        should return True for questions with 0 <= publication date <= 1 days old.
        """
        time = timezone.now() - datetime.timedelta(hours=20)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)

    def test_was_published_recently_with_future_question(self):
        """
        should return False for questions with a publication date in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls-index'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['questions'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls-index'))
        self.assertQuerysetEqual(
            response.context['questions'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls-index'))
        # self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['questions'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls-index'))
        self.assertQuerysetEqual(
            response.context['questions'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls-index'))
        self.assertQuerysetEqual(
            response.context['questions'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls-detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls-detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
