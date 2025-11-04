import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# from main_app.models import Recipe

# recipe = Recipe(
#     name = "Chicken and Rice",
#     description = "Chicken and rice with a nice dressing",
#    ingredients = "Chicken, Rice, Dressing",
#     cook_time = 10
# ) # Create a new object
# recipe.save() # Save the recipe to the database
# Create queries within functions
