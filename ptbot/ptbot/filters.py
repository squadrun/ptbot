import datetime

from django.contrib.admin import SimpleListFilter, DateFieldListFilter
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ptbot.models import Story, Person


class OwnerFilter(SimpleListFilter):
    title = _('Owner')
    parameter_name = 'owners'

    def lookups(self, request, model_admin):
        list_of_list_of_owners = Story.objects.all().values_list("owners", flat=True)
        list_of_all_owners = []
        for list_of_owners in list_of_list_of_owners:
            if list_of_owners:
                list_of_all_owners.extend(list_of_owners)
        set_of_owners = set(list_of_all_owners)

        return [
            (person_id, person_name) for person_id, person_name in
            Person.objects.filter(id__in=set_of_owners).values_list("id", "name").order_by("name")
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(owners__contains=[self.value()])


class CustomDateFieldListFilter(DateFieldListFilter):
    def __init__(self, *args, **kwargs):
        super(CustomDateFieldListFilter, self).__init__(*args, **kwargs)

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        today = now.date()
        tomorrow = today + datetime.timedelta(days=1)
        self.insert_in_links(3, ((
            (_('Past 14 days'), {
                self.lookup_kwarg_since: str(today - datetime.timedelta(days=14)),
                self.lookup_kwarg_until: str(tomorrow),
            }),
        )))

    def insert_in_links(self, position, item):
        self.links = self.links[:position] + item + self.links[position:]
