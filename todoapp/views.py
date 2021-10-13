import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from .constants import *
from .db_interaction import TodoDBInteraction
from .mappers import Mappers


@api_view([GET_METHOD, POST_METHOD])
@csrf_exempt
def generalToDo(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == GET_METHOD:
            flag = request.GET.get(FLAGS_FIELD, '')
            name = request.GET.get(NAME_FIELD, '')
            if flag == '' and name == '':
                status_code, response = TodoDBInteraction.getAllToDo(user)
                return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status_code)
            elif flag == '':
                status_code, response = TodoDBInteraction.getToDoByName(name, user)
                return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status_code)
            elif name == '':
                status_code, response = TodoDBInteraction.getToDoByFlag(flag, user)
                return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status_code)
            else:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        elif request.method == POST_METHOD:
            payload = json.loads(request.body)
            todo_object = Mappers.mapNewToDo(payload, request.user)

            if type(todo_object) == NameError:
                response = json.dumps(([{ERROR_KEY: str(todo_object)}]))
                return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status.HTTP_406_NOT_ACCEPTABLE)

            status_code, response = TodoDBInteraction.save(todo_object)
            return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status_code)
    return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@api_view([GET_METHOD, PUT_METHOD, DELETE_METHOD])
@csrf_exempt
def todoById(request, todo_id):
    if request.user.is_authenticated:
        user = request.user
        if request.method == GET_METHOD:
            retrieved_todo = TodoDBInteraction.getToDoById(todo_id, user)
            if retrieved_todo == status.HTTP_204_NO_CONTENT:
                return HttpResponse(status=status.HTTP_204_NO_CONTENT)
            return HttpResponse(retrieved_todo, content_type=CONTENT_TYPE_JSON, status=status.HTTP_200_OK)

        elif request.method == PUT_METHOD:
            retrieved_todo = TodoDBInteraction.getToDoById(todo_id, user)

            payload = json.loads(request.body)

            if retrieved_todo == status.HTTP_204_NO_CONTENT:
                response = json.dumps(([{ERROR_KEY: NO_TODO_MSG}]))
                return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status.HTTP_404_NOT_FOUND)

            todo_to_update = Mappers.mapUpdatedToDo(payload, retrieved_todo, user)

            if type(todo_to_update) == NameError:
                response = json.dumps(([{ERROR_KEY: str(todo_to_update)}]))
                return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status.HTTP_406_NOT_ACCEPTABLE)

            status_code, response = TodoDBInteraction.update(todo_to_update)
            return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status_code)

        elif request.method == DELETE_METHOD:
            status_code, response = TodoDBInteraction.deleteToDO(todo_id, user)
            return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status_code)
    return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


@api_view([GET_METHOD, POST_METHOD, PUT_METHOD, DELETE_METHOD])
@csrf_exempt
def user_management(request):
    if request.method == POST_METHOD:
        payload = json.loads(request.body)
        user_to_add = Mappers.map_new_user(payload)

        if type(user_to_add) == NameError:
            response = json.dumps(([{ERROR_KEY: str(user_to_add)}]))
            return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status.HTTP_406_NOT_ACCEPTABLE)

        status_code, response = TodoDBInteraction.save_user(user_to_add)
        return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status_code)

    elif request.user.is_authenticated:
        user = request.user

        if request.method == PUT_METHOD:
            payload = json.loads(request.body)

            user_to_update = Mappers.map_update_user(payload, user)

            if type(user_to_update) == NameError:
                response = json.dumps(([{ERROR_KEY: str(user_to_update)}]))
                return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status.HTTP_406_NOT_ACCEPTABLE)

            status_code, response = TodoDBInteraction.update_user(user_to_update, user.id)
            return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status_code)

        elif request.method == DELETE_METHOD:
            status_code, response = TodoDBInteraction.delete_user(user)
            return HttpResponse(response, content_type=CONTENT_TYPE_JSON, status=status_code)

        elif request.method == GET_METHOD:

            user_json = Mappers.get_map_user(user)
            return HttpResponse(user_json, content_type=CONTENT_TYPE_JSON, status=status.HTTP_200_OK)

