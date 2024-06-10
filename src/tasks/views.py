from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from src.tasks.models import Task
from src.tasks.permissions import IsEmployee
from src.tasks.serializers import TaskSerializer, CreateTaskByEmployeeSerializer, \
    CreateTaskByCustomerSerializer, CompleteTaskSerializer, TaskUpdateSerializer


class TaskViewSet(GenericViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'employee':
            return Task.objects.filter(status='awaits_performer') | Task.objects.filter(employee=user)
        return Task.objects.filter(customer=user)

    def get_serializer_class(self):
        if self.action == 'create':
            user = self.request.user
            if not user.is_anonymous:  # to see correct body in the swagger
                if user.user_type == 'employee':
                    return CreateTaskByEmployeeSerializer
                elif user.user_type == 'customer':
                    return CreateTaskByCustomerSerializer
        return TaskSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(self.get_serializer(task).data, status=status.HTTP_201_CREATED)


class TaskUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskUpdateSerializer

    def get_object(self):
        try:
            return Task.objects.get(pk=self.kwargs['uuid'])
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        return Task.objects.filter(uuid=self.kwargs['uuid'])

    def update(self, request, *args, **kwargs):
        task = self.get_object()

        if task.status == 'awaits_performer':
            if request.user == task.customer:
                return super().update(request, *args, **kwargs)
            else:
                return Response({'error': 'You have no permission to edit this task.'},
                                status=status.HTTP_403_FORBIDDEN)

        elif task.status == 'in_progress':
            if request.user == task.employee:
                return super().update(request, *args, **kwargs)
            else:
                return Response({'error': 'Only employee that took this task can edit it.'},
                                status=status.HTTP_403_FORBIDDEN)

        return Response({'error': 'You cannot edit a completed task.'}, status=status.HTTP_403_FORBIDDEN)


class TakeTaskView(APIView):
    permission_classes = [IsEmployee]

    def patch(self, request, uuid):
        try:
            task = Task.objects.get(uuid=uuid, status='awaits_performer')
        except Task.DoesNotExist:
            return Response({'error': 'Task not found or not in awaits_performer status'},
                            status=status.HTTP_404_NOT_FOUND)

        task.status = 'in_progress'
        task.employee = request.user
        task.save()

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompleteTaskView(GenericAPIView):
    permission_classes = [IsEmployee]
    serializer_class = CompleteTaskSerializer

    def patch(self, request, uuid):
        try:
            task = Task.objects.get(uuid=uuid, status='in_progress')
        except Task.DoesNotExist:
            return Response({'error': 'Task not found or not in in_progress status'},
                            status=status.HTTP_404_NOT_FOUND)

        if task.employee != request.user:
            return Response({'error': 'You are not the assigned for this task'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(task, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
