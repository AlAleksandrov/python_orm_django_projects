import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Sum, F, Avg
from main_app.models import Astronaut, Mission, Spacecraft


# Create queries within functions
def get_astronauts(search_string=None) -> str:
    if search_string is None:
        return ''

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by(
        'name'
    )

    if not astronauts:
        return ''

    return '\n'.join(
        f'Astronaut: {a.name}, phone number: {a.phone_number}, status: {"Active" if a.is_active else "Inactive"}'
        for a in astronauts
    )

def get_top_astronaut() -> str:
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not astronaut or astronaut.missions_count == 0:
        return 'No data.'

    return f'Top Astronaut: {astronaut.name} with {astronaut.missions_count} missions.'

def get_top_commander() -> str:
    commander = Astronaut.objects.annotate(
        commanded_missions_count=Count(
            'commanded_missions'
        )
    ).order_by(
            '-commanded_missions_count',
            'phone_number'
        ).first()

    if commander and commander.commanded_missions_count > 0:
        return f'Top Commander: {commander.name} with {commander.commanded_missions_count} commanded missions.'

    return 'No data.'


def get_last_completed_mission() -> str:
    last_completed_mission = Mission.objects.select_related(
        'spacecraft',
        'commander'
    ).prefetch_related(
        'astronauts'
    ).filter(
        status=Mission.StatusDefined.COMPLETED
    ).order_by(
        '-launch_date'
    ).first()

    if not last_completed_mission:
        return 'No data.'

    commander_name = last_completed_mission.commander.name if last_completed_mission.commander else 'TBA'
    astronauts_name = ', '.join(a.name for a in last_completed_mission.astronauts.order_by('name'))
    spacecraft_name = last_completed_mission.spacecraft.name
    total_spacewalks = last_completed_mission.astronauts.order_by('name').aggregate(total=Sum('spacewalks'))['total']

    return (f"The last completed mission is: {last_completed_mission.name}. "
            f"Commander: {commander_name}. "
            f"Astronauts: {astronauts_name}. "
            f"Spacecraft: {spacecraft_name}. "
            f"Total spacewalks: {total_spacewalks}.")

def get_most_used_spacecraft() -> str:
    spacecraft = Spacecraft.objects.annotate(
        count_missions=Count('used_in_missions', distinct=True),
        count_astronauts=Count('used_in_missions__astronauts', distinct=True)
    ).order_by(
        '-count_missions',
        'name'
    ).first()

    if not spacecraft or spacecraft.count_missions == 0:
        return 'No data.'

    return (f"The most used spacecraft is: {spacecraft.name}, "
            f"manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.count_missions} missions, "
            f"astronauts on missions: {spacecraft.count_astronauts}.")

def decrease_spacecrafts_weight() -> str:
    spacecrafts = Spacecraft.objects.filter(
        weight__gt=200.0,
        used_in_missions__status=Mission.StatusDefined.PLANNED
    ).distinct()

    if not spacecrafts:
        return 'No changes in weight.'

    spacecrafts.update(weight=F('weight') - 200.0)

    avg_weight = Spacecraft.objects.aggregate(
        avg_weight=Avg('weight')
    )['avg_weight']

    return (f"The weight of {spacecrafts.count()} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")