import pytest
from pytest_django.asserts import TestCase
from django.test import Client
from django.urls import reverse, reverse_lazy
from .models import Exercise, ExerciseInstance
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestFitness:
    username = 'dummyusername'
    password = 'testing321'
    client = Client()

    @pytest.fixture(autouse=True)
    def setup_stuff(self):
        # Strangely, could not access the database to create a user in the class scope, despite @pytest.mark.django_db
        # being sufficient for model objects like Exercise/ExerciseInstance. This setup fixture is the workaround.
        global user     # needs to be global to be accessible to the test functions
        user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        Exercise.objects.create(name='Bicep Curl', type='db')
        ExerciseInstance.objects.create(name=Exercise.objects.all()[0], sets=5, reps=5, weight=5, user=user)

    def test_exercise_create(self):
        assert Exercise.objects.create(name='Test Exercise', type='db')

    def test_exercise_instance_create(self):
        assert ExerciseInstance.objects.create(name=Exercise.objects.all()[0], sets=5, reps=5, weight=5, user=user)

    def test_exercise_instance_volume_method(self):
        assert ExerciseInstance.objects.all()[0].volume() == 25

    def test_fitness_home_response(self):
        assert self.client.get(reverse('fitness-home')).status_code == 200

    def test_fitness_progress_response(self):
        assert self.client.get(reverse('fitness-progress', kwargs={'exercise_name': 'Bicep Curl'})).status_code == 200

    def test_fitness_create_response(self):
        assert self.client.get(reverse('fitness-create')).status_code == 200

    def test_fitness_update_response(self):
        assert self.client.get(reverse('fitness-update', kwargs={'pk': 1})).status_code == 200
