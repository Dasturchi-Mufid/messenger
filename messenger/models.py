from django.db import models
from django.contrib.auth.models import User

import string
from random import sample


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True,unique=True)
    
    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15)) 
    
    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Group(CodeGenerate):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='member_groups', blank=True)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
            super(Group, self).save(*args, **kwargs)
            self.members.add(self.admin)

class JoinRequest(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Join request from {self.user.username} to {self.group.name}"


    def save(self, *args, **kwargs):
        join_request = JoinRequest.objects.filter(
            user=self.user, 
            group=self.group,
            is_active=True
            ).count()
        if not join_request:
            super(JoinRequest,self).save(*args, **kwargs)
class Message(CodeGenerate):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} ({self.time}): {self.content[:50]}..."

    
    def save(self, *args, **kwargs):
        if self.sender in self.group.members.all():
            super(Message, self).save(*args, **kwargs)

