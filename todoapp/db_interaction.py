from django.contrib.auth.models import User
from rest_framework import status

from .utils import *


class TodoDBInteraction:

    @staticmethod
    def save(obj_to_save):
        try:
            obj_to_save.save()
            response = json.dumps([{SUCCESS_KEY: SUCCESSFULLY_CREATED_MSG}])
            return status.HTTP_201_CREATED, response
        except Exception as exp:
            response = json.dumps([{ERROR_KEY: str(exp)}])
            return status.HTTP_400_BAD_REQUEST, response

    @staticmethod
    def save_user(user_to_save):
        try:
            User.objects.get_or_create(username=user_to_save[USER_NAME_FIELD],
                                       password=user_to_save[PASSWORD_FIELD],
                                       first_name=user_to_save[FIRST_NAME_FIELD],
                                       last_name=user_to_save[LAST_NAME_FIELD],
                                       email=user_to_save[EMAIL_FIELD])
            response = json.dumps([{SUCCESS_KEY: SUCCESSFULLY_CREATED_MSG}])
            return status.HTTP_201_CREATED, response
        except Exception as exp:
            response = json.dumps([{ERROR_KEY: str(exp)}])
            return status.HTTP_400_BAD_REQUEST, response

    @staticmethod
    def getAllToDo(user_instance):
        try:
            todo = Todo.objects.filter(user=user_instance)
            response = format_response(todo, user_instance)
            response = create_reminder_alert(response)
            return status.HTTP_200_OK, response
        except Exception as exp:
            serialized_response = TodoSerializer(None, many=False)
            return status.HTTP_204_NO_CONTENT, json.dumps(serialized_response.data)

    @staticmethod
    def getToDoById(todo_id, user_instance):
        try:
            todo = Todo.objects.filter(pk=todo_id, user=user_instance)
            response = format_response(todo, user_instance)
            return create_reminder_alert(response)
        except Exception as exp:
            return status.HTTP_204_NO_CONTENT

    @staticmethod
    def getToDoByName(todo_name, user_instance):
        try:
            todo = Todo.objects.filter(name=todo_name, user=user_instance)
            response = format_response(todo, user_instance)
            response = create_reminder_alert(response)
            return status.HTTP_200_OK, response
        except Exception as exp:
            serialized_response = TodoSerializer(None, many=False)
            return status.HTTP_204_NO_CONTENT, json.dumps(serialized_response.data)

    @staticmethod
    def getToDoByFlag(todo_flag, user_instance):
        try:
            all_todo_from_flag = Todo.objects.filter(user=user_instance)
            filtered_todo_by_flag = filter_flag(all_todo_from_flag, todo_flag)
            response = format_response(filtered_todo_by_flag, user_instance)
            response = create_reminder_alert(response)
            return status.HTTP_200_OK, response
        except Exception as exp:
            serialized_response = TodoSerializer(None, many=False)
            return status.HTTP_204_NO_CONTENT, json.dumps(serialized_response.data)

    @staticmethod
    def getToDoUpdate(todo_id, user_instance):
        try:
            todo = Todo.objects.filter(pk=todo_id, user=user_instance)
            serialized_response = TodoSerializer(todo)
            response = json.dumps(serialized_response.data)
            return response
        except Exception as exp:
            return status.HTTP_204_NO_CONTENT

    @staticmethod
    def update(obj_to_update):
        try:
            obj_to_update.save()
            response = json.dumps([{SUCCESS_KEY: UPDATED_MSG}])
            return status.HTTP_200_OK, response
        except Exception as exp:
            error_description = json.dumps(({ERROR_KEY: UPDATE_ERROR_MSG}))
            return status.HTTP_400_BAD_REQUEST, error_description

    @staticmethod
    def updateStatus(todo_id):
        todo = Todo.objects.get(pk=todo_id)
        todo.status = STATUS_FIELD_DONE
        todo.save()

    @staticmethod
    def updateToDo(todo):
        try:
            todo.save()
            response = json.dumps([{SUCCESS_KEY: UPDATED_MSG}])
            return status.HTTP_200_OK, response
        except Exception as exp:
            error_description = json.dumps(({ERROR_KEY: UPDATE_ERROR_MSG}))
            return status.HTTP_400_BAD_REQUEST, error_description

    @staticmethod
    def update_user(user_to_update, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.username = user_to_update[USER_NAME_FIELD]
            user.first_name = user_to_update[FIRST_NAME_FIELD]
            user.last_name = user_to_update[LAST_NAME_FIELD]
            user.email = user_to_update[EMAIL_FIELD]
            user.save()
            response = json.dumps([{SUCCESS_KEY: SUCCESSFULLY_CREATED_MSG}])
            return status.HTTP_201_CREATED, response
        except Exception as exp:
            response = json.dumps([{ERROR_KEY: str(exp)}])
            return status.HTTP_400_BAD_REQUEST, response

    @staticmethod
    def deleteToDO(todo_id, user_instance):
        try:
            todo = Todo.objects.get(pk=todo_id, user=user_instance)
            todo.delete()
            response = json.dumps([{SUCCESS_KEY: TODO_REMOVED_MSG}])
            return status.HTTP_200_OK, response
        except Exception as exp:
            error_description = json.dumps(({ERROR_KEY: TODO_DELETION_ERROR_MSG}))
            return status.HTTP_400_BAD_REQUEST, error_description

    @staticmethod
    def delete_user(user):
        try:
            user.delete()
            response = json.dumps([{SUCCESS_KEY: USER_REMOVED_MSG}])
            return status.HTTP_200_OK, response
        except Exception as exp:
            error_description = json.dumps(({ERROR_KEY: USER_DELETION_ERROR_MSG}))
            return status.HTTP_400_BAD_REQUEST, error_description
