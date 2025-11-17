from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json

from .models import Task
from .forms import TaskForm


def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "completed": task.completed,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
    }


@csrf_exempt
def task_list_create(request):
    if request.method == "GET":
        tasks = Task.objects.order_by('-created_at')
        data = [serialize_task(t) for t in tasks]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode() or '{}')
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        form = TaskForm(payload)
        if form.is_valid():
            task = form.save()
            return JsonResponse(serialize_task(task), status=201)
        return JsonResponse({"errors": form.errors}, status=400)

    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "GET":
        return JsonResponse(serialize_task(task))

    if request.method in ("PUT", "PATCH"):
        try:
            payload = json.loads(request.body.decode() or '{}')
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        form = TaskForm(payload, instance=task)
        if form.is_valid():
            task = form.save()
            return JsonResponse(serialize_task(task))
        return JsonResponse({"errors": form.errors}, status=400)

    if request.method == "DELETE":
        task.delete()
        return JsonResponse({"deleted": True})

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])


@csrf_exempt
def task_toggle(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return JsonResponse(serialize_task(task))
