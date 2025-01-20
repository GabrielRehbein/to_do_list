from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication
from .models import Task
from rest_framework.request import Request
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from .filters.posted_filters import filter_by_posted
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    def get(self, request: Request) -> Response:
        """
        Mostra apenas as tasks que foram postadas.
        """

        
        tasks = filter_by_posted(request)
        
        serializer = TaskSerializer(tasks, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    
    def post(self, request: Request) -> Response:
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )


class TaskRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    def get(self, request: Request, id: str) -> Response:
        
        task = get_object_or_404(Task, id=id)
        serializer = TaskSerializer(task)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, id) -> Response:
        task = Task.objects.get(id=id)
        data = request.data
        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

    def delete(self, request: Request, id) -> Response:
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except:
            Response(
                data='Task not found.',
                status=status.HTTP_404_NOT_FOUND
            )
