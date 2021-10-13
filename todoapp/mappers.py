import json
from datetime import datetime

from django.contrib.auth.hashers import make_password

from .constants import *
from .models import Todo
from .serializers import CurrentUserSerializer
from .utils import check_date_format


def _check_input_fields_todo(payload):
    if ((payload[NAME_FIELD] is None or payload[NAME_FIELD] == "") and
            (payload[DESCRIPTION_FIELD] is None or payload[DESCRIPTION_FIELD] == "") and
            (payload[STATUS_FIELD] is None or payload[STATUS_FIELD] == "") and
            (payload[DUE_FIELD] is None or payload[DUE_FIELD] == "") and
            (payload[REMINDER_FIELD] is None or payload[REMINDER_FIELD] == "") and
            (payload[FLAGS_FIELD] is None or payload[FLAGS_FIELD] == "")):
        return False
    else:
        return True


def _check_input_fields_user(payload):
    if ((payload[USER_NAME_FIELD] is None or payload[USER_NAME_FIELD] == "") and
            (payload[FIRST_NAME_FIELD] is None or payload[FIRST_NAME_FIELD] == "") and
            (payload[LAST_NAME_FIELD] is None or payload[LAST_NAME_FIELD] == "") and
            (payload[PASSWORD_FIELD] is None or payload[PASSWORD_FIELD] == "") and
            (payload[EMAIL_FIELD] is None or payload[EMAIL_FIELD] == "")):
        return False
    else:
        return True


class Mappers:

    @staticmethod
    def mapNewToDo(payload, user_instance):
        if not _check_input_fields_todo(payload):
            NameError(REQUIRED_FIELDS_ERR0R_MSG)

        name = payload[NAME_FIELD]
        description = payload[DESCRIPTION_FIELD]
        user = user_instance
        todo_status = payload[STATUS_FIELD]
        reminder = payload[REMINDER_FIELD]
        created = datetime.now()
        edited = datetime.now()
        due = check_date_format(payload[DUE_FIELD])
        flags = payload[FLAGS_FIELD]
        if due < created:
            return NameError(DUE_DATE_ERR0R_MSG)

        if len(list(flags)) > 5:
            return NameError(FLAG_NUMBER_ERR0R_MSG)

        return Todo(name=name, description=description, user=user, created=created,
                    edited=edited, status=todo_status, due=due, reminder=reminder, flags=flags)

    @staticmethod
    def map_new_user(payload):
        if not _check_input_fields_user(payload):
            NameError(REQUIRED_FIELDS_ERR0R_MSG)

        payload[PASSWORD_FIELD] = make_password(payload[PASSWORD_FIELD])
        return payload

    @staticmethod
    def mapUpdatedToDo(payload, retrieved_to_do, user):
        json_keys = payload.keys()
        json_retrieved_todo_object = json.loads(retrieved_to_do)[0]

        for key in json_keys:

            if key not in [NAME_FIELD, DESCRIPTION_FIELD, STATUS_FIELD, REMINDER_FIELD, FLAGS_FIELD, DUE_FIELD]:
                return NameError(WRONG_FIELD_ERROR_MSG.format(str(key)))

            if key == DUE_FIELD:
                if check_date_format(payload[DUE_FIELD]) < datetime.now():
                    return NameError(DUE_DATE_ERR0R_MSG)

            if key == FLAGS_FIELD and len(list(payload[FLAGS_FIELD])) > 5:
                return NameError(FLAG_NUMBER_ERR0R_MSG)

            if payload.get(key) == "":
                return NameError(EMPTY_FIELD_ERROR_MSG.format(key))

            json_retrieved_todo_object[key] = payload[key]

        return Todo(id=json_retrieved_todo_object[ID_FIELD], name=json_retrieved_todo_object[NAME_FIELD],
                    description=json_retrieved_todo_object[DESCRIPTION_FIELD],
                    user=user, created=json_retrieved_todo_object[CREATED_FIELD],
                    edited=datetime.now(), status=json_retrieved_todo_object[STATUS_FIELD],
                    due=check_date_format(json_retrieved_todo_object[DUE_FIELD]),
                    reminder=json_retrieved_todo_object[REMINDER_FIELD],
                    flags=json_retrieved_todo_object[FLAGS_FIELD])

    @staticmethod
    def map_update_user(payload, user):
        json_keys = payload.keys()
        serialized = CurrentUserSerializer(user)
        json_user_object = json.loads(json.dumps(serialized.data))

        for key in json_keys:
            if payload.get(key) == "":
                return NameError(EMPTY_FIELD_ERROR_MSG.format(key))

            json_user_object[key] = payload[key]

        return json_user_object

    @staticmethod
    def get_map_user(user):
        serialized_user = CurrentUserSerializer(user)
        return json.dumps(serialized_user.data)
