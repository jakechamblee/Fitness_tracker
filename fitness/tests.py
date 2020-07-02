import pytest
from pytest_django.asserts import TestCase
from django.test import Client
from django.urls import reverse, reverse_lazy
from .models import Exercise, ExerciseInstance
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestFitnessResponses:

    def test_fitness_home(self):
        username = 'testusername'
        password = 'testing321'
        client = Client()
        User.objects.create_user(username=username, password=password)
        client.login(username=username, password=password)
        assert client.get(reverse('fitness-home')).status_code == 200

    # def test_fitness_progress(self):
    #     client = Client()
    #     assert client.get(reverse('fitness-progress', kwargs={'exercise_name': 'Plank'})).status_code == 200

    def test_fitness_progress(self):
        client = Client()
        assert client.get('/fitness/progress/Plank/').status_code == 200

    def test_fitness_create(self):
        username = 'testusername'
        password = 'testing321'
        client = Client()
        User.objects.create_user(username=username, password=password)
        client.login(username=username, password=password)
        assert client.get('/fitness/fitness_create_form/').status_code == 200

    def test_fitness_update(self):
        username = 'testusername'
        password = 'testing321'
        client = Client()
        User.objects.create_user(username=username, password=password)
        client.login(username=username, password=password)
        assert client.get(reverse('fitness-update', kwargs={'pk': 30})).status_code == 200


# def test_fitness_create_form():


# def create_ExerciseInstance():
#     ex_instance = ExerciseInstance.objects.create(date_performed='', )

# def create_Exercise():