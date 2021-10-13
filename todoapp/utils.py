import json
from datetime import datetime

from .constants import *
from .models import Todo
from .serializers import TodoSerializer, CurrentUserSerializer


def check_date_format(date_str):
    try:
        date_obj = datetime.strptime(date_str, DATE_FORMAT_STR)
        return date_obj
    except ValueError(DATE_FORMAT_ERROR_MSG) as date_error:
        raise date_error


def format_date_response(date_str):
    return date_str[0:10] + " " + date_str[11:16]


def updateStatus(todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.status = STATUS_FIELD_DONE
    todo.save()


def create_reminder_alert(todo):
    todo_json = json.loads(todo)

    for todo_item in todo_json:
        todo_item[CREATED_FIELD] = format_date_response(todo_item[CREATED_FIELD])
        todo_item[EDITED_FIELD] = format_date_response(todo_item[EDITED_FIELD])
        todo_item[DUE_FIELD] = format_date_response(todo_item[DUE_FIELD])

        reminder = int(todo_item[REMINDER_FIELD])
        due_datetime = datetime.strptime(todo_item[DUE_FIELD], DATE_FORMAT_STR)
        now_datetime = datetime.now()

        remaining_time = int((due_datetime - now_datetime).total_seconds() / 60)
        if reminder >= 0 and remaining_time < 0:
            updateStatus(todo_item[ID_FIELD])
            todo_item[REMINDER_WRN] = EXPIRED_TODO_REMINDER_MSG
            todo_item[STATUS_FIELD] = STATUS_FIELD_DONE
        elif reminder >= 0 and remaining_time <= reminder:
            todo_item[REMINDER_WRN] = REMINDER_WRN_MSG.format(remaining_time)

    return json.dumps(todo_json)


def filter_flag(db_response, flag_name):
    response_items = []
    for item in db_response:
        if flag_name in item.flags:
            response_items.append(item)
    return response_items


def format_response(todo, user):
    serialized_response = TodoSerializer(todo, many=True)
    response = get_user(json.dumps(serialized_response.data), user)
    return response


def get_user(todo, user):
    serialized_user = CurrentUserSerializer(user)
    user_json = json.loads(json.dumps(serialized_user.data))
    todo_json = json.loads(todo)
    for todo_obj in todo_json:
        todo_obj[USER_FIELD] = user_json
    return json.dumps(todo_json)
