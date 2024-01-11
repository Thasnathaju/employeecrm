from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from api.serializers import EmployeeSerializer,TaskSerializer
from api.models import Employees,Tasks
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import authentication,permissions



class EmployeeModelViewSetView(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAdminUser]
    authentication_classes=[authentication.TokenAuthentication]

    serializer_class=EmployeeSerializer
    model=Employees
    queryset=Employees.objects.all()

    #localhost:8000/api/v2/employee/departments/
    #method:put

    def list(self, request, *args, **kwargs):
        qs=Employees.objects.all()
       # http://127.0.0.1:8000/api/v2/employees/?department=hr
        print(request.query_params)#{department:hr}
        if "department" in request.query_params:
            value=request.query_params.get("department")
            qs=qs.filter(department=value)
        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["get"],detail=False)

    def departments(self,request,*args,**kwargs):
        data=Employees.objects.all().values_list("department",flat=True).distinct()
        return Response(data=data)

    @action(methods=["post"],detail=True)

    def add_task(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        employee_object=Employees.objects.get(id=id)
        serializer=TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee_object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

#list all task for a specific employee         
#lh:8000/api/v2/employees/{id}/tasks/
#method:Get
    @action(methods=["get"],detail=True)    
    def tasks(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Tasks.objects.filter(employee__id=id)
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)

class TaskViewSetView(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        task_object=Tasks.objects.get(id=id)
        serializer=TaskSerializer(data=request.data,instance=task_object)
        if serializer.is_valid():
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
#lh:8000/api/v2/task/{taskid}/
#method:Get    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Tasks.objects.get(id=id)
        serializer=TaskSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Tasks.objects.get(id=id).delete()
        return Response(data={"message":"delete"})



    
        
        

    