from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Borrar datos existentes
        Activity.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        # Equipos
        marvel = Team.objects.create(name='Marvel', universe='Marvel')
        dc = Team.objects.create(name='DC', universe='DC')

        # Usuarios
        ironman = User.objects.create(email='ironman@marvel.com', name='Iron Man', team=marvel)
        spiderman = User.objects.create(email='spiderman@marvel.com', name='Spider-Man', team=marvel)
        batman = User.objects.create(email='batman@dc.com', name='Batman', team=dc)
        superman = User.objects.create(email='superman@dc.com', name='Superman', team=dc)

        # Actividades
        Activity.objects.create(user=ironman, type='Running', duration=30, date=date.today())
        Activity.objects.create(user=spiderman, type='Cycling', duration=45, date=date.today())
        Activity.objects.create(user=batman, type='Swimming', duration=60, date=date.today())
        Activity.objects.create(user=superman, type='Yoga', duration=50, date=date.today())

        # Workouts
        w1 = Workout.objects.create(name='Full Body', description='Entrenamiento completo')
        w2 = Workout.objects.create(name='Cardio Blast', description='Cardio intenso')
        w1.suggested_for.set([marvel, dc])
        w2.suggested_for.set([marvel])

        # Leaderboard
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        # Índice único en email (colección users)
        with connection.cursor() as cursor:
            cursor.execute('db.users.createIndex({ "email": 1 }, { "unique": true })')

        self.stdout.write(self.style.SUCCESS('Base de datos octofit_db poblada con datos de ejemplo.'))
