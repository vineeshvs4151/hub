# from re import T
from django.shortcuts import render
# Create your views here.
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.serializer import RegistrationSerializer, TodoSerializer
from api.models import Todos
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

class TodosView(ViewSet):

    def list(self,request,*args,**kw):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else: 
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=TodoSerializer(qs,many=False)
        return Response(data=serializer.data)

    def destory(self,request,*args,**kw):
        id=kw.get("pk")
        Todos.objects.filter(id=id).delete()
        return Response(data="Deleted")

    def update(self,request,*args,**kw):
        id=kw.get("pk")  
        qs=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=qs)   
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)  


class TodoModelView(ModelViewSet):  
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TodoSerializer
    queryset= Todos.objects.all() 

    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)    

         


    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user) 
    
    # def create(self,request,*args,**kw):
    #     serializer=TodoSerializer(data=request.data) 
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

    # def list(self,request,*args,**kw):  
    #     us=request.user
    #     qs=Todos.objects.filter(user=us)
    #     serializer=TodoSerializer(qs,many=True)  
    #     return Response(data=serializer.data)
    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)    
   
    @action(methods=["GET"],detail=False)
    def pending_todo(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False) 
        serializer=TodoSerializer(qs,many=True)  
        return Response(data=serializer.data)  

    @action(methods=["GET"],detail=False)
    def completed_todo(self,request ,*args,**kw):
        qs=Todos.objects.filter(status=True)   
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data) 
    
    @action(methods=["GET"],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        # qs= Todos.objects.filter(id=id).update(status=True)
        qs=Todos.objects.get(id=id)
        qs.status=True
        qs.save( )
        serializer=TodoSerializer(qs,many=False)
        return Response(data=serializer.data )


class UserView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()

    # def create(self,request,*args,**kw):
    #     serializer=RegistratSerionializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)    
    #     else:
    #         return Response(data=serializer.errors)    