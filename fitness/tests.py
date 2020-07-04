import pytest
from pytest_django.asserts import TestCase
from django.test import Client
from django.urls import reverse, reverse_lazy
from .models import Exercise, ExerciseInstance
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestFitnessResponses:
    username = 'dummyusername'
    password = 'testing321'
    client = Client()

    @pytest.fixture(autouse=True)
    def setup_stuff(self, db):
        # For some reason, could not access the database to create a user, despite @pytest.mark.django_db
        # being sufficient for model objects like Exercise/ExerciseInstance. This setup function is the workaround.
        global user
        user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        Exercise.objects.create(name='Bicep Curl', type='db')
        ExerciseInstance.objects.create(name=Exercise.objects.all()[0], sets=5, reps=5, weight=5, user=user)

    def test_fitness_home(self):
        assert self.client.get(reverse('fitness-home')).status_code == 200

    def test_fitness_progress(self):
        assert self.client.get(reverse('fitness-progress', kwargs={'exercise_name': 'Bicep Curl'})).status_code == 200

    def test_fitness_create(self):
        assert self.client.get(reverse('fitness-create')).status_code == 200

    def test_fitness_update(self):
        assert self.client.get(reverse('fitness-update', kwargs={'pk': 1})).status_code == 200
