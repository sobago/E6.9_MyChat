from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import *
from .models import *


class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


def index(request):
    return render(request, 'chat/index.html', {
        'rooms': Room.objects.all(),
        'users': User.objects.all()
    })


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'old_messages': Message.objects.filter(chat=get_room(room_name)).order_by('-id')[:10][::-1]
    })


def get_room(name):
    try:
        return Room.objects.get(title=name)

    except ObjectDoesNotExist:
        return None
