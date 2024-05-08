from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers
from messenger import models

@api_view(['GET'])
def group_list(request):
    groups = models.Group.objects.all()
    serializer_data = serializers.GroupSerializer(groups,many=True)
    return Response(serializer_data.data)


@api_view(['POST'])
def group_create(request):
    group_name = request.data.get('name')
    admin_id = request.data.get('admin')
    admin = models.User.objects.get(id=admin_id)
    group = models.Group.objects.create(name=group_name, admin=admin)
    group.members.add(admin)
    serializer_data = serializers.GroupSerializer(group)
    return Response(serializer_data.data)


@api_view(['GET'])
def search_groups(request):
    q = request.data.get('q')
    groups = models.Group.objects.filter(name__icontains=q)
    serializer_data = serializers.GroupSerializer(groups,many=True)
    return Response(serializer_data.data)