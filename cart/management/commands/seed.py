from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from cart.models import Item, Order
from movies.models import Movie

# region, index into the movie list, quantity
SALES = [
    ('GA', 0, 4),
    ('CA', 1, 6),
    ('NY', 2, 3),
    ('TX', 0, 5),
    ('FL', 1, 2),
    ('AL', 2, 7),
]


class Command(BaseCommand):
    help = 'Create sample orders in a few states so the sales map has data.'

    def handle(self, *args, **options):
        movies = list(Movie.objects.all())
        if not movies:
            self.stdout.write(self.style.WARNING(
                'No movies in the database. Add movies in admin, then run this again.'))
            return

        user, created = User.objects.get_or_create(username='mapseed')
        if created:
            user.set_unusable_password()
            user.save()

        if Order.objects.filter(user=user).exists():
            self.stdout.write('Sample region sales already exist. Nothing added.')
            return

        for region, movie_index, quantity in SALES:
            movie = movies[movie_index % len(movies)]
            order = Order(
                user=user,
                total=movie.price * quantity,
                region=region,
            )
            order.save()
            Item.objects.create(
                price=movie.price,
                quantity=quantity,
                order=order,
                movie=movie,
            )

        self.stdout.write(self.style.SUCCESS(
            'Added sample sales for GA, CA, NY, TX, FL, and AL.'))