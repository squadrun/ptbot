from django.contrib.postgres.fields import ArrayField
from django.db import models

from ptbot.constants import PROJECT_API_LINK, ACCOUNT_API_LINK, PERSON_API_LINK, STORY_API_LINK
from ptbot.mapper import PROJECT_MAPPER, ACCOUNT_MAPPER, PERSON_MAPPER, STORY_MAPPER


class CreateUpdateAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, help_text="Object creation date")
    updated_at = models.DateTimeField(auto_now=True, help_text="Object updation date")

    class Meta:
        abstract = True


class Account(CreateUpdateAbstractModel):
    id = models.PositiveIntegerField(primary_key=True, help_text="Account ID on PT")
    name = models.CharField(max_length=64, help_text="Account name on PT")
    plan = models.CharField(max_length=16, help_text="Account plan")
    status = models.CharField(max_length=16, help_text="Account status")
    created_on = models.DateTimeField(help_text="Date and time when this account was created")

    @classmethod
    def get_mapper(cls):
        return ACCOUNT_MAPPER

    @classmethod
    def get_api_links(cls):
        return [ACCOUNT_API_LINK]


class Project(CreateUpdateAbstractModel):
    id = models.PositiveIntegerField(primary_key=True, help_text="Project ID on PT")
    account = models.ForeignKey(Account, help_text="Account ID under which this project exists")
    name = models.CharField(max_length=64, help_text="Project name on PT")
    project_type = models.CharField(max_length=16, help_text="Type of the project")
    timezone_olson_name = models.CharField(max_length=32, help_text="Project timezone olson name")
    timezone_offset = models.CharField(max_length=16, help_text="Project timezone offset")
    iteration_length = models.PositiveSmallIntegerField(help_text="Length of a single iteration for this project")
    iterations_done = models.PositiveSmallIntegerField(help_text="Number of iterations done in this project")
    current_iteration = models.PositiveSmallIntegerField(help_text="Current iteration number for this project")
    created_on = models.DateTimeField(help_text="Date and time when this project was created")

    def __unicode__(self):
        return self.name

    @classmethod
    def get_mapper(cls):
        return PROJECT_MAPPER

    @classmethod
    def get_api_links(cls):
        return [PROJECT_API_LINK]


class Person(CreateUpdateAbstractModel):
    id = models.PositiveIntegerField(primary_key=True, help_text="Person's ID on PT")
    name = models.CharField(max_length=64, help_text="Person's name on PT")
    username = models.CharField(max_length=64, help_text="Person's username on PT")
    email = models.EmailField(max_length=64, help_text="Person's email ID on PT")

    def __unicode__(self):
        return self.username

    @classmethod
    def get_mapper(cls):
        return PERSON_MAPPER

    @classmethod
    def get_api_links(cls):
        project_ids = Project.objects.all().values_list('id', flat=True)
        return [PERSON_API_LINK.format(project_id=id) for id in project_ids]


class Story(CreateUpdateAbstractModel):
    id = models.PositiveIntegerField(primary_key=True, help_text="Story ID on PT")
    project = models.ForeignKey(Project, help_text="Project to which this story belongs")
    name = models.CharField(max_length=256, help_text="Story title on PT")
    description = models.TextField(help_text="Story description on PT")
    story_type = models.CharField(max_length=16, help_text="Type of the story")
    story_url = models.URLField(help_text="PT URL for the story")
    requestor = models.ForeignKey(Person, help_text="Person who has requested this story")
    owners = ArrayField(models.PositiveIntegerField(), help_text="Persons who own this story")
    estimate = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Story point estimation of the story")
    current_state = models.CharField(max_length=16, help_text="Current status of the story")
    labels = ArrayField(models.CharField(max_length=256), help_text="Labels applied on the story")
    created_on = models.DateTimeField(help_text="Date and Time when the story was created")
    updated_on = models.DateTimeField(help_text="Date and Time when the story was updated")
    accepted_on = models.DateTimeField(blank=True, null=True, help_text="Date and Time when the story was accpeted")

    @classmethod
    def get_mapper(cls):
        return STORY_MAPPER

    @classmethod
    def get_api_links(cls):
        project_ids = Project.objects.all().values_list('id', flat=True)
        return [STORY_API_LINK.format(project_id=id) for id in project_ids]
