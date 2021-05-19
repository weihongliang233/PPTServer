import errno
import json
import os

import django.core.exceptions
from django.db.models.query import QuerySet
from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from user import models

from . import models

User = models.User
# Create your views here.

def download(useID_toMe)->FileResponse:
    instance: User =User.objects.get(userID=useID_toMe)
    file=open(instance.filename,'rb')
    response = FileResponse(file)
    response['Content-Type']='application/octet-stream'
    return response

def testProcess(request: HttpRequest):
    method = request.method
    action = request.headers.get("action")
    if method == "GET":
        request.params = request.GET      
        if action == "query":
            oneUser=UserOperators(request)
            queryResult=oneUser.query()
            return JsonResponse(queryResult,safe=False)

        elif action=="download":
            download_student_ID=request.params["userID"]
            return download(download_student_ID)
            
        elif action=="query_students_belong_to_One_Tearcher":
            oneTeacher=Teacher(request)
            students=oneTeacher.query_students_belong_to_me()
            print(students)
            return JsonResponse({"students": students},safe=False)
    
    elif method == "POST":
        dataType = request.headers.get("content-type")#根据數據類型分類處理
        if dataType == "application/json":
            request.params = json.loads(request.body)          
        else:
            request.params = request.POST   
        
        if action == "modifyPassword":
            newpassword = request.params['newpassword']
            oneUser = UserOperators(request)
            modifyPasswordResult=oneUser.modifyPassword(newpassword)
            return JsonResponse(modifyPasswordResult,safe=False)
        elif action == "upload":
            oneStudent=Student(request)
            filename=request.params['filename']
            oneStudent.upload(filename)
            return HttpResponse("Success")
        elif action == "addStudent":
            oneTeacher=Teacher(request)
            ref = oneTeacher.addStudent(request.params['addData'])
            if(ref):
                return JsonResponse({"msg":"success"},safe=False)
            else:
                return JsonResponse({"msg":"faile"},safe=False)
    else:
        return HttpResponse("Erro")



class UserOperators:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.Id: str = self.request.params['userID']
        self.Identity: str = self.check()

    def check(self) -> str:
        password: str = self.request.params['password']
        
        #其實可以用filter()
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
            return {"msg":"success"}
        else:
            return {"msg":"faile"}

    def query(self):
        if self.Identity == "Student" or self.Identity == 'Teacher':
            instance: QuerySet = User.objects.filter(userID=self.Id) 
            info = instance.values('Name', 'School', 'Group', 'Identity')[0]
            return info


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
        
        instance: User = User.objects.get(userID=self.Id)
        instance.filename=filenameAndPath 
        instance.save()
        return "Success"


class Teacher(UserOperators):
    def __init__(self, request: HttpRequest) -> None:
        super().__init__(request)
        if self.Identity == 'Teacher':
            instance: User = User.objects.get(userID=self.Id)
            self.School: str = instance.School
            self.Group: str = instance.Group
            self.Teacher_Name:str=instance.Name
    
    def addStudent(self, info: dict): 
        #for key,value in self.request.params.items():
        #    User.objects.create(eval("key = value"))
        User.objects.create(
            userID=info['userID'],
            Name=info['Name'],
            School=info['School'],
            Group=info['Group'],
            password='12345',
            filename=info['userID']+' File',
            Identity=info['Identity'],
            Teacher=self.Teacher_Name
        )
        return True

    def query_students_belong_to_me(self):
        students_object=User.objects.filter(Teacher=self.Teacher_Name)
        students=students_object.values('userID','Name','Group')
        return list(students)