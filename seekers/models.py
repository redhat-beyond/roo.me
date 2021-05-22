from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from roo_me.settings import AUTH_USER_MODEL
from apartments.models import Apartment
from contacts.models import Connection


class Seeker(models.Model):
    base_user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    city = models.ForeignKey('apartments.City', on_delete=models.RESTRICT, related_name='city_seekers')
    start_date = models.DateField()
    min_rent = models.IntegerField()
    max_rent = models.IntegerField()
    num_of_roomates = models.IntegerField()
    num_of_rooms = models.IntegerField()
    about = models.TextField(blank=True)

    def __str__(self):
        return f"Seeker:{self.base_user}"

    def get_matched_apartments(self):
        apartments = self.get_all_relevant_apartments()
        return sorted(
            apartments,
            key=lambda apt: apt.owner.get_matching_score(self.base_user),
            reverse=True
        )

    '''TODO: Delete this function and use the search function from the search application instead.
    This is a temporary function - it was only written in order to develop the feature.
    DO NOT USE once the search application is merged.'''
    def get_all_relevant_apartments(self):

        filter_args = {
                'is_relevant': True,
                'city': self.city,
                'rent__lte': self.max_rent,
                'rent__gte': self.min_rent,
                'num_of_roomates__lte': self.num_of_roomates,
                'num_of_rooms': self.num_of_rooms,
            }

        if self.base_user.not_smoking:
            filter_args['owner__not_smoking'] = True
        if self.base_user.pets_allowed:
            filter_args['owner__pets_allowed'] = True
        if self.base_user.air_conditioner:
            filter_args['owner__air_conditioner'] = True
        if self.base_user.balcony:
            filter_args['owner__balcony'] = True
        if self.base_user.elevator:
            filter_args['owner__elevator'] = True
        if self.base_user.long_term:
            filter_args['ownner__long_term'] = True
        if self.base_user.immediate_entry:
            filter_args['owner__immediate_entry'] = True

        relevant_apartments = Apartment.objects.filter(**filter_args)
        for apartment in relevant_apartments:
            try:
                Connection.objects.get(seeker=self, apartment=apartment)
                relevant_apartments = relevant_apartments.exclude(pk=apartment.pk)
            except ObjectDoesNotExist:
                pass

        return relevant_apartments
