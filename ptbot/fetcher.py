import json

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from ptbot.mapper import resolve_mappings
from ptbot.models import Project, Account, Person, Story

models = (Account, Project, Person, Story)


def fetch_data(token):
    for model in models:
        api_links = model.get_api_links()
        for api_link in api_links:
            response = requests.get(api_link, headers={'X-TrackerToken': token})
            if response.status_code == status.HTTP_200_OK:
                try:
                    response_json = json.loads(response.text)
                except ValueError:
                    pass
                else:
                    if type(response_json) == list:
                        for item in response_json:
                            create_or_update_object(model, item)
                    else:
                        create_or_update_object(model, response_json)
            else:
                print response.status_code


def create_or_update_object(model, api_data):
    resolved_data = resolve_data_for_model(model, resolve_mappings(api_data, model.get_mapper()))

    object_filter = model.objects.filter(id=resolved_data["id"])
    if object_filter.exists():
        object_filter.update(**resolved_data)
    else:
        model.objects.create(**resolved_data)


def resolve_data_for_model(model, data):
    model_fields = model._meta.get_fields()

    related_model_fields_dict = {}
    model_fields_name_list = []
    for field in model_fields:
        if field.related_model:
            related_model_fields_dict[field.name] = field.related_model
        else:
            model_fields_name_list.append(field.name)

    resolved_data = {}
    for key in data:
        if key in model_fields_name_list:
            resolved_data[key] = data[key]
        elif key in related_model_fields_dict:
            related_model = related_model_fields_dict[key]

            related_field_pk_value = data[key]
            try:
                resolved_data[key] = related_model.objects.get(pk=related_field_pk_value)
            except ObjectDoesNotExist as e:
                print e

    return resolved_data
