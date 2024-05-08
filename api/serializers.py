from messenger import models
from rest_framework.serializers import ModelSerializer

class GroupSerializer(ModelSerializer):
    class Meta:
        model = models.Group
        fields = '__all__'
        
