from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Exercise(models.Model):
    name = models.CharField(
        max_length=100,
        help_text='Enter a name for the exercise (e.g. Bench Press).'
    )

    LIFT_TYPE = (
        ('db', 'Dumbbell'),
        ('bb', 'Barbell'),
        ('bw', 'Bodyweight'),
    )

    type = models.CharField(max_length=15, choices=LIFT_TYPE, default='db',
                            help_text='Enter "db", "bb" or "bw"')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class ExerciseInstance(models.Model):
    date_performed = models.DateField(default=timezone.now)
    name = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    sets = models.PositiveSmallIntegerField(default=0)
    reps = models.PositiveSmallIntegerField(default=0, help_text="Enter the average")
    weight = models.DecimalField(default=0, decimal_places=1, max_digits=5,
                                 help_text='Enter the weight of each dumbbell or the whole barbell')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_performed', 'name']

    def __str__(self):
        return f'{self.name} for {self.user} on {self.date_performed:%B %d, %Y}'

    def volume(self):
        return int(self.sets*self.reps)

    def get_absolute_url(self):
        return reverse('fitness-home')


class Workout(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return f'{self.name} workout'


