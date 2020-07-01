import pytest
from pytest_django.asserts import TestCase
from django.test import Client
from .models import Exercise, ExerciseInstance

class TestFitnessResponses:
    c = Client()
    c.login(username='testuser', password='testing321'
    def test_fitness_home(self):
        assert c.get('/fitness/').status_code == 200

    def test_fitness_progress(self):
        assert c.get('/fitness/progress/Plank/').status_code == 200

    def test_fitness_create(self):
        assert c.get('/fitness/fitness_create_form/').status_code == 200

    def test_fitness_update(self):
        assert c.get('/fitness/update/30/').status_code == 200


# def create_ExerciseInstance():
#     ex_instance = ExerciseInstance.objects.create(date_performed='', )

# def create_Exercise():


