import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom
from django.db.models import QuerySet
from decimal import Decimal
from typing import Optional
from main_app.choices import RoomTypeChoice
# Create queries within functions

def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(
        name=name,
        species=species
    )

    return f"{pet.name} is a very cute {pet.species}!"

# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"

def rename_artifact(artifact: Artifact, new_name: str) -> None:
    if artifact.age > 250 and artifact.is_magical:
        artifact.name = new_name
        artifact.save()

def delete_all_artifacts() -> None:
    artifact = Artifact.objects.all()
    artifact.delete()

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)


def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')

    return '\n'.join(f'{l.name} has a population of {l.population}!' for l in locations)

def new_capital() -> None:
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()

def get_capitals() -> QuerySet:
    return Location.objects.filter(is_capital=True)

def delete_first_location() -> None:
    first_location = Location.objects.first()
    first_location.delete()

# print(show_all_locations())
# print(new_capital())
# print(get_capitals())


def apply_discount() -> None:
    cars = Car.objects.all()

    for c in cars:
        discount = Decimal(str(sum(int(d) for d in str(c.year)) / 100))
        c.price_with_discount = c.price * (1 - discount)
        c.save()

def get_recent_cars() -> QuerySet:
    recent_cars = Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')

    return recent_cars

def delete_last_car() -> None:
    Car.objects.last().delete()

# apply_discount()
# print(get_recent_cars())


def show_unfinished_tasks() -> str:
    tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(f'Task - {t.title} needs to be done until {t.due_date}!' for t in tasks)

def complete_odd_tasks() -> None:
    # tasks = Task.objects.filter(is_finished=False).filter(id__mod=2)
    # tasks.update(is_finished=True)
    # tasks.save()

    tasks = Task.objects.all()
    completed_tasks = []
    for t in tasks:
        if t.id % 2 != 0:
            t.is_finished = True
            completed_tasks.append(t)

    Task.objects.bulk_update(completed_tasks, ['is_finished'])

def encode_and_replace(text: str, task_title: str) -> None:
    encoded_text = ''.join(chr(ord(l) - 3) for l in text)

    # Option 1: python loop -> worst
    for task in Task.objects.filter(title=task_title):
        task.description = encoded_text
        task.save()

    # Option 3: direct update -> best ->
    Task.objects.filter(title=task_title).update(description=encoded_text)

# encode_and_replace("Zdvk#wkh#glvkhv$", "Sample Task")
# print(Task.objects.get(title='Sample Task').description)


def get_deluxe_rooms() -> str|None:
    deluxe_rooms = HotelRoom.objects.filter(room_type=RoomTypeChoice.DELUXE).values('room_number', 'price_per_night')
    if deluxe_rooms.id % 2 == 0:
        return '\n'.join(f'Deluxe room with number {dr.room_number} costs {dr.price_per_night}$ per night!' for dr in deluxe_rooms)
    return None

def increase_room_capacity() -> None:
    reserved_rooms = HotelRoom.objects.filter(is_reserved=True).order_by('id')
    previous_room : Optional[HotelRoom] = None

    for r in reserved_rooms:
        if previous_room:
            r.capacity += previous_room.capacity
        else:
            r.capacity += r.id

        previous_room = r
        r.save()

def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()

def delete_last_room() -> None:
    room = HotelRoom.objects.last()
    if not room.is_reserved:
        room.delete()

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)
