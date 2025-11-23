import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, F, Count, Min, Avg
from main_app.models import House, Dragon, Quest


# Create queries within functions

def get_houses(search_string=None) -> str:
    houses = House.objects.filter(
        Q(name__istartswith=search_string)
            |
        Q(motto__istartswith=search_string)
    ).order_by(
        '-wins',
        'name'
    )

    if not houses or not search_string:
        return "No houses match your search."

    if not houses.motto:
        houses.motto = 'N/A'

    return '\n'.join(f'House: {houses.name}, wins: {houses.wins}, motto: {houses.motto}')

def get_most_dangerous_house() -> str:
    most_dangerous_house = House.objects.get_houses_by_dragons_count().first()

    if not most_dangerous_house or not most_dangerous_house.dragon_count:
        return "No relevant data."

    return f"The most dangerous house is the House of {most_dangerous_house.name} \
            with {most_dangerous_house.dragon_count} dragons. \
            Currently {'' if most_dangerous_house.is_ruling else 'not '}ruling the kingdom."

def get_most_powerful_dragon() -> str:
    powerful_dragon = Dragon.objects.filter(
        is_healthy=True,
        power__lte=10.0
    ).order_by(
        '-power',
        'name'
    ).first()

    if not powerful_dragon:
        return "No relevant data."

    return f"The most powerful healthy dragon is {powerful_dragon.name} \
            with a power level of {powerful_dragon.power:.1f}, \
            breath type {powerful_dragon.breath}, and {powerful_dragon.wins} wins, \
            coming from the house of {powerful_dragon.house.name}. \
            Currently participating in {powerful_dragon.quests.count()} quests."


def update_dragons_data() -> str:
    injured_dragons = Dragon.objects.filter(
        count=Count('affected_dragons'),
        is_healthy=False,
        power__gt=1.0
    ).order_by(
        '-power',
        'name'
    ).update(
        power=F('power') - 0.1,
        is_healthy=True
    )
    min_power = Dragon.objects.aggregate(min_power=Min('power'))['min_power']

    if not injured_dragons:
        return "No changes in dragons data."

    return f"The data for {injured_dragons.count} dragon/s has been changed. \
            The minimum power level among all dragons is {min_power:.1f}"

def get_earliest_quest() -> str:
    earliest_quest = Quest.objects.order_by(
        'start_time'
    ).first()

    if not earliest_quest:
        return "No relevant data."

    host_name = earliest_quest.host.name
    dragon_name = '*'.join(dragon.name for dragon in earliest_quest.dragons.all().order_by('-power', 'name'))
    avg_power_level = earliest_quest.dragons.aggregate(Avg('power'))['power__avg']

    return f"The earliest quest is: {earliest_quest.name},\
            code: {earliest_quest.code},\
            start date: {earliest_quest.start_time.day}.{earliest_quest.start_time.month}.{earliest_quest.start_time.year},\
            host: {host_name}. \
            Dragons: {dragon_name}. \
            Average dragons power level: {avg_power_level:.2f}"

def announce_quest_winner(quest_code) -> str:
    quest = Quest.objects.select_related(
        'host'
    ).prefetch_related(
        'dragons'
    ).filter(
        code=quest_code
    ).first()

    if not quest:
        return "No such quest."

    dragon_winner = quest.dragons.order_by('-power', 'name').first()
    dragon_winner.update(wins=F('wins') + 1)
    dragon_winner.house.update(wins=F('wins') + 1)
    quest_name = quest.name
    dragon_name = dragon_winner.name
    house_name = quest.host.name
    dragon_wins = dragon_winner.wins
    house_wins = quest.host.wins
    quest_reward = quest.reward
    quest.delete()

    return f"The quest: {quest_name} has been won by dragon {dragon_name} from house { house_name}. \
            The number of wins has been updated as follows: {dragon_wins} \
            total wins for the dragon and {house_wins} total wins for the house. \
            The house was awarded with {quest_reward} coins."
