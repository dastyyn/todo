from rest_framework.decorators import api_view
from rest_framework.response import Response
from todolist.models import Task
from .serializers import TaskSerializer, TaskValidateSerializer
from rest_framework import status


@api_view(['GET', 'POST'])
def task_list_api_view(request):
    if request.method == 'GET':
        task_list = Task.objects.all()
        data = TaskSerializer(task_list, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = TaskValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
        title = request.data.get('title')
        description = request.data.get('description')
        completed = request.data.get('completed')
        task = Task.objects.create(title=title, description=description, completed=completed)
        return Response(status=status.HTTP_201_CREATED, data={'task_id': task.id})


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail_api_view(request, id):
    try:
        task_detail = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response(data={'error_message': 'Task does not'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = TaskSerializer(task_detail).data
        return Response(data=data)
    elif request.method == 'PUT':
        task_detail.title = request.data.get('title')
        task_detail.description = request.data.get('description')
        task_detail.completed = request.data.get('completed')
        task_detail.save()
        return Response(status=status.HTTP_201_CREATED, data={'task_id': task_detail.id})
    else:
        task_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
