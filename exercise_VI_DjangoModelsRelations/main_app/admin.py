from django.contrib import admin

from main_app.models import Car


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'year', 'owner', 'car_details')

    def car_details(self, obj: object):
        try:
            owner_name = obj.owner.name
        except AttributeError:
            owner_name = 'No owner'

        try:
            plate = obj.registration.registration_number
        except AttributeError:
            plate = 'No registration number'

        return f'Owner: {owner_name}, Registration: {plate}'

    car_details.short_description = 'Car details'