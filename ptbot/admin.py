from django.contrib import admin
from django.utils.html import format_html

from ptbot.filters import OwnerFilter, CustomDateFieldListFilter
from ptbot.models import Account, Project, Person, Story


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'plan', 'status', 'created_on')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'iteration_length', 'iterations_done', 'current_iteration', 'created_on')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'email')


class StoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'project', 'name', 'get_owners', 'current_state', 'estimate', 'story_type', 'get_story_url', 'created_on',
        'updated_on', 'accepted_on'
    )
    search_fields = ("id",)
    list_filter = (OwnerFilter, "current_state", "project", "story_type", ("accepted_on", CustomDateFieldListFilter),
                   ("updated_on", CustomDateFieldListFilter))

    def get_story_url(self, obj=None):
        return format_html("<a href={url} target=\"_blank\">{url}</a>".format(url=obj.story_url))

    def get_owners(self, obj=None):
        list_of_owners = Person.objects.filter(id__in=obj.owners).values_list("name", flat=True)
        return ", ".join(list_of_owners)

    get_story_url.short_description = "Story URL"
    get_owners.short_description = "Owners"


admin.site.register(Account, AccountAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Story, StoryAdmin)
