from user import models
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . import models
import django.core.exceptions
import os
import errno

User = models.User
# Create your views here.


def testProcess(request: HttpRequest):
    action = request.headers.get("action")
    if action == "check":
        oneUser=UserOperators(request)
        checkResult=oneUser.check()
        return HttpResponse(checkResult)
    
    elif action == "modifyPassword":
        newpassword = request.headers.get('newpassword')
        oneUser = UserOperators(request)
        modifyPasswordResult=oneUser.modifyPassword(newpassword)
        return HttpResponse(modifyPasswordResult)

    elif action == "query":
        oneUser=UserOperators(request)
        content=request.headers.get("content")
        queryResult=oneUser.query(content)
        return HttpResponse(queryResult)

    elif action == 'upload':
        oneStudent=Student(request)
        filename=request.headers.get('filename')
        oneStudent.upload(filename)
        return HttpResponse("Success")
    else:
        return HttpResponse("Can't match any action")



class UserOperators:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.Id: str = self.request.headers.get("userID")
        self.Identity: str = self.check()

    def check(self) -> str:
        password: str = self.request.headers.get("password")

        try:
            instance: User = User.objects.get(userID=self.Id)
        except django.core.exceptions.ObjectDoesNotExist:
            return "No ID exist"
        else:
            if instance.password == password:
                return instance.Identity
            else:
                return "password does not match"

    def modifyPassword(self, newpassword: str) -> str:
        if self.Identity == "Student" or self.Identity == 'Teacher':
            instance: User = User.objects.get(userID=self.Id)
            instance.password = newpassword
            instance.save()
            return instance.password
        else:
            return "You can't modify password"

    def query(self, content: str):
        if self.Identity == "Student" or self.Identity == 'Teacher':
            instance: User = User.objects.get(userID=self.Id)
            return eval("instance." + content)


class Student(UserOperators):
    def __init__(self, request: HttpRequest) -> None:
        super().__init__(request)
        if self.Identity == 'Student':
            instance: User = User.objects.get(userID=self.Id)
            self.School: str = instance.School
            self.Group: str = instance.Group

    def upload(self, filename: str):
        file = self.request.FILES['file']
        filenameAndPath: str = './FileStore/' + self.School + '/' + self.Group + '/' + filename

        if not os.path.exists(os.path.dirname(filenameAndPath)):
            try:
                os.makedirs(os.path.dirname(filenameAndPath))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filenameAndPath, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return "Success"
# fuck you