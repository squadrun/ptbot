NESTED_DATA = "nested_data"
NESTING_MAP_DELIMITER = "."

ACCOUNT_MAPPER = {
    "created_at": "created_on"
}

PROJECT_MAPPER = {
    "number_of_done_iterations_to_show": "iterations_done",
    "current_iteration_number": "current_iteration",
    "created_at": "created_on",
    "account_id": "account",

    NESTED_DATA: {
        "timezone_olson_name": "time_zone" + NESTING_MAP_DELIMITER + "olson_name",
        "timezone_offset": "time_zone" + NESTING_MAP_DELIMITER + "offset"
    }
}

PERSON_MAPPER = {
    NESTED_DATA: {
        "id": "person" + NESTING_MAP_DELIMITER + "id",
        "name": "person" + NESTING_MAP_DELIMITER + "name",
        "email": "person" + NESTING_MAP_DELIMITER + "email",
        "username": "person" + NESTING_MAP_DELIMITER + "username"
    }
}

STORY_MAPPER = {
    "url": "story_url",
    "requested_by_id": "requestor",
    "owner_ids": "owners",
    "created_at": "created_on",
    "updated_at": "updated_on",
    "accepted_at": "accepted_on",
    "project_id": "project",

    NESTED_DATA: {
        "labels": "labels" + NESTING_MAP_DELIMITER + "name"
    }
}


def resolve_mappings(api_data_dict, mapper):
    resolved_data_dict = {}

    for key in mapper:
        if key == NESTED_DATA or key not in api_data_dict:
            continue

        new_mapping_key = mapper[key]
        resolved_data_dict[new_mapping_key] = api_data_dict[key]
        del api_data_dict[key]

    if NESTED_DATA in mapper:
        resolve_nested_data(resolved_data_dict, api_data_dict, mapper)

    resolved_data_dict.update(api_data_dict)
    return resolved_data_dict


def resolve_nested_data(resolved_data_dict, api_data_dict, mapper):
    nesting = mapper[NESTED_DATA]

    for item in nesting:
        nesting_map = nesting[item]
        resolved_data_dict[item] = fetch_nested_data(api_data_dict, nesting_map)

    return resolved_data_dict


def fetch_nested_data(api_data_dict, nesting_map):
    nesting_map_list = nesting_map.split(NESTING_MAP_DELIMITER)
    data = api_data_dict
    for key in nesting_map_list:
        if type(data) == list:
            data = [item[key] for item in data]
        else:
            data = data[key]

    return data
