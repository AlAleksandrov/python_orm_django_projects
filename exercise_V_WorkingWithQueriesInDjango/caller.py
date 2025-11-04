import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout
from typing import List
from main_app.choices import OperationSystemsChoices, LaptopBrandChoices, MealTypeChoices, DungeonDifficultyChoices, \
    WorkoutTypeChoices
from django.db.models import When, Case, Value, F, TextField, CharField, IntegerField, QuerySet


# Create and check models
# Run and print your queries


def show_highest_rated_art() -> str:
    highest_rating = ArtworkGallery.objects.all().order_by('-rating', 'id').first()

    return f'{highest_rating.art_name} is the highest-rated art with a {highest_rating.rating} rating!'

def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])

def delete_negative_rated_arts() -> None:
    ArtworkGallery.objects.filter(rating__lt=0).delete()

# populate_model_with_data(ArtworkGallery)
# print(show_highest_rated_art())

# artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)
#
# # Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())


def show_the_most_expensive_laptop() -> str:
    laptop = Laptop.objects.all().order_by('-price', '-id').first()
    return f'{laptop.brand} is the most expensive laptop available for {laptop.price}$!'

def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)

def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).filter(storage__lt=512).update(storage=512)

def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).filter(memory__lt=16).update(memory=16)

def update_operation_systems() -> None:
    # Option 1
    Laptop.objects.update(
        operation_system=Case(
            When(brand=LaptopBrandChoices.ASUS, then=Value(OperationSystemsChoices.WINDOWS)),
            When(brand=LaptopBrandChoices.APPLE, then=Value(OperationSystemsChoices.MAC_OS)),
            When(brand=LaptopBrandChoices.LENOVO, then=Value(OperationSystemsChoices.CHROME_OS)),
            When(brand__in=[
                    LaptopBrandChoices.DELL, LaptopBrandChoices.ACER
                ], then=Value(OperationSystemsChoices.LINUX)
            ),
        )
    )

    # Option 2
    # Laptop.objects.filter(brand=LaptopBrandChoices.ASUS).update(operation_system=OperationSystemsChoices.WINDOWS)
    # Laptop.objects.filter(brand=LaptopBrandChoices.APPLE).update(operation_system=OperationSystemsChoices.MAC_OS)
    # Laptop.objects.filter(brand__in=[LaptopBrandChoices.DELL, LaptopBrandChoices.ACER]).update(operation_system=OperationSystemsChoices.LINUX)
    # Laptop.objects.filter(brand=LaptopBrandChoices.LENOVO).update(operation_system=OperationSystemsChoices.CHROME_OS)

def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()

# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )
#
# # Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
#
# # Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)
#
# update_to_512_GB_storage()
# update_operation_systems()
#
# # Retrieve 2 laptops from the database
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()
#
# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)


def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)

def delete_chess_players() -> None:
    ChessPlayer.objects.filter(title='no title').delete()

def change_chess_games_won() -> None:
    ChessPlayer.objects.filter(title='GM').update(games_won=30)

def change_chess_games_lost() -> None:
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)

def change_chess_games_drawn() -> None:
    ChessPlayer.objects.update(games_drawn=10)

def grand_chess_title_GM() -> None:
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')

def grand_chess_title_IM() -> None:
    ChessPlayer.objects.filter(rating__gte=2300, rating__lte=2399).update(title='IM')

def grand_chess_title_FM() -> None:
    ChessPlayer.objects.filter(rating__gte=2200, rating__lte=2299).update(title='FM')

def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__lte=2199).update(title='regular player')


# player1 = ChessPlayer(
#     username='Player1',
#     title='no title',
#     rating=2200,
#     games_played=50,
#     games_won=20,
#     games_lost=25,
#     games_drawn=5,
# )
# player2 = ChessPlayer(
#     username='Player2',
#     title='IM',
#     rating=2350,
#     games_played=80,
#     games_won=40,
#     games_lost=25,
#     games_drawn=15,
# )
#
# # Call the bulk_create_chess_players function
# bulk_create_chess_players([player1, player2])
#
# # Call the delete_chess_players function
# delete_chess_players()
#
# # Check that the players are deleted
# print("Number of Chess Players after deletion:", ChessPlayer.objects.count())


def set_new_chefs() -> None:
    Meal.objects.filter(meal_type=MealTypeChoices.BREAKFAST).update(chef='Gordon Ramsay')
    Meal.objects.filter(meal_type=MealTypeChoices.LUNCH).update(chef='Julia Child')
    Meal.objects.filter(meal_type=MealTypeChoices.DINNER).update(chef='Jamie Oliver')
    Meal.objects.filter(meal_type=MealTypeChoices.SNACK).update(chef='Thomas Keller')

def set_new_preparation_times() -> None:
    Meal.objects.filter(meal_type=MealTypeChoices.BREAKFAST).update(preparation_time='10 minutes')
    Meal.objects.filter(meal_type=MealTypeChoices.LUNCH).update(preparation_time='12 minutes')
    Meal.objects.filter(meal_type=MealTypeChoices.DINNER).update(preparation_time='15 minutes')
    Meal.objects.filter(meal_type=MealTypeChoices.SNACK).update(preparation_time='5 minutes')

def update_low_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.BREAKFAST, MealTypeChoices.DINNER]).update(calories=400)

def update_high_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).update(calories=700)

def delete_lunch_and_snack_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).delete()

# meal1 = Meal.objects.create(
#     name="Pancakes",
#     meal_type="Breakfast",
#     preparation_time="20 minutes",
#     difficulty=3,
#     calories=350,
#     chef="Jane",
# )
#
# meal2 = Meal.objects.create(
#     name="Spaghetti Bolognese",
#     meal_type="Dinner",
#     preparation_time="45 minutes",
#     difficulty=4,
#     calories=550,
#     chef="Sarah",
# )
# # Test the set_new_chefs function
# set_new_chefs()
#
# # Test the set_new_preparation_times function
# set_new_preparation_times()
#
# # Refreshes the instances
# meal1.refresh_from_db()
# meal2.refresh_from_db()
#
# # Print the updated meal information
# print("Meal 1 Chef:", meal1.chef)
# print("Meal 1 Preparation Time:", meal1.preparation_time)
# print("Meal 2 Chef:", meal2.chef)
# print("Meal 2 Preparation Time:", meal2.preparation_time)


def show_hard_dungeons() -> str:
    hard_dungeons = Dungeon.objects.filter(difficulty=DungeonDifficultyChoices.HARD).order_by('-location')
    return '\n'.join(f'{hd.name} is guarded by {hd.boss_name} who has {hd.boss_health} health points!' for hd in hard_dungeons)

def bulk_create_dungeons(args: List[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)

def update_dungeon_names() -> None:
    Dungeon.objects.update(
        name=Case(
            When(difficulty=DungeonDifficultyChoices.EASY, then=Value('The Erased Thombs')),
            When(difficulty=DungeonDifficultyChoices.MEDIUM, then=Value('The Coral Labyrinth')),
            When(difficulty=DungeonDifficultyChoices.HARD, then=Value('The Lost Haunt')),
            default=F('name')
        )
    )

def update_dungeon_bosses_health() -> None:
    Dungeon.objects.exclude(difficulty=DungeonDifficultyChoices.EASY).update(boss_health=500)

def update_dungeon_recommended_levels() -> None:
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty=DungeonDifficultyChoices.EASY, then=Value(25)),
            When(difficulty=DungeonDifficultyChoices.MEDIUM, then=Value(50)),
            When(difficulty=DungeonDifficultyChoices.HARD, then=Value(75)),
            default=F('recommended_level'),
            output_field=IntegerField()
        )
    )

def update_dungeon_rewards() -> None:
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then=Value('1000 Gold')),
            When(location__startswith="E", then=Value('New dungeon unlocked')),
            When(location__endswith="s", then=Value('Dragonheart Amulet')),
            default=F('reward'),
            output_field=TextField()
        )
    )

def set_new_locations() -> None:
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss')),
            default=F('location')
        )
    )


# # Create two instances
# dungeon1 = Dungeon(
#     name="Dungeon 1",
#     boss_name="Boss 1",
#     boss_health=1000,
#     recommended_level=75,
#     reward="Gold",
#     location="Eternal Hell",
#     difficulty="Hard",
# )
#
# dungeon2 = Dungeon(
#     name="Dungeon 2",
#     boss_name="Boss 2",
#     boss_health=400,
#     recommended_level=25,
#     reward="Experience",
#     location="Crystal Caverns",
#     difficulty="Easy",
# )
#
# # Bulk save the instances
# bulk_create_dungeons([dungeon1, dungeon2])
#
# # Update boss's health
# update_dungeon_bosses_health()
#
# # Show hard dungeons
# hard_dungeons_info = show_hard_dungeons()
# print(hard_dungeons_info)
#
# # Change dungeon names based on difficulty
# update_dungeon_names()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].name)
# print(dungeons[1].name)
#
# # Change the dungeon rewards
# update_dungeon_rewards()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].reward)
# print(dungeons[1].reward)


def show_workouts() -> str:
    workouts=Workout.objects.filter(workout_type__in=[WorkoutTypeChoices.CALISTHENICS, WorkoutTypeChoices.CROSSFIT]).order_by('id')
    return '\n'.join(F'{w.name} from {w.workout_type} type has {w.difficulty} difficulty!' for w in workouts)

def get_high_difficulty_cardio_workouts() -> QuerySet:
    return Workout.objects.filter(workout_type=WorkoutTypeChoices.CARDIO, difficulty=DungeonDifficultyChoices.HARD).order_by('instructor')

def set_new_instructors() -> None:
    Workout.objects.update(
        instructor=Case(
            When(workout_type=WorkoutTypeChoices.CARDIO, then=Value('John Smith')),
            When(workout_type=WorkoutTypeChoices.STRENGTH, then=Value('Michael Williams')),
            When(workout_type=WorkoutTypeChoices.YOGA, then=Value('Emily Johnson')),
            When(workout_type=WorkoutTypeChoices.CROSSFIT, then=Value('Sarah Davis')),
            When(workout_type=WorkoutTypeChoices.CALISTHENICS, then=Value('Chris Heria')),
        )
    )

def set_new_duration_times() -> None:
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes')),
        )
    )

def delete_workouts() -> None:
    Workout.objects.exclude(workout_type__in=[WorkoutTypeChoices.STRENGTH, WorkoutTypeChoices.CALISTHENICS]).delete()


# # Create two Workout instances
# workout1 = Workout.objects.create(
#     name="Push-Ups",
#     workout_type="Calisthenics",
#     duration="10 minutes",
#     difficulty="Intermediate",
#     calories_burned=200,
#     instructor="Bob"
# )
#
# workout2 = Workout.objects.create(
#     name="Running",
#     workout_type="Cardio",
#     duration="30 minutes",
#     difficulty="High",
#     calories_burned=400,
#     instructor="Lilly"
# )
#
# # Run the functions
# print(show_workouts())
#
# high_difficulty_cardio_workouts = get_high_difficulty_cardio_workouts()
# for workout in high_difficulty_cardio_workouts:
#     print(f"{workout.name} by {workout.instructor}")
#
# set_new_instructors()
# for workout in Workout.objects.all():
#     print(f"Instructor: {workout.instructor}")
#
# set_new_duration_times()
# for workout in Workout.objects.all():
#     print(f"Duration: {workout.duration}")

