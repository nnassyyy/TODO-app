from fastapi import APIRouter, HTTPException, Depends
from src.repositories.task_repository import InMemoryTaskRepository
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.domain.task import Task
from .dependencies import get_task_repository

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, operation_id="create_task_item")
def create_task(
    task_data: TaskCreate,
    repo: InMemoryTaskRepository = Depends(get_task_repository)
):
    try:
        task = Task(task_data.title, task_data.project_id)
        for tag in task_data.tags:
            task.add_tag(tag)
        created_task = repo.create(task)
        return TaskResponse(
            id=created_task.id,
            title=created_task.title,
            is_completed=created_task.is_completed,
            tags=list(created_task.tags),
            project_id=created_task.project_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    repo: InMemoryTaskRepository = Depends(get_task_repository)
):
    task = repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(
        id=task.id,
        title=task.title,
        is_completed=task.is_completed,
        tags=list(task.tags),
        project_id=task.project_id
    )


@router.get("/{task_id}/history")
def get_task_history(
        task_id: int,
        repo: InMemoryTaskRepository = Depends(get_task_repository)
):
    task = repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.get_history()


@router.get("", response_model=list[TaskResponse])
def get_tasks(
        tags: str = None,
        completed: bool = None,
        project_id: int = None,
        repo: InMemoryTaskRepository = Depends(get_task_repository)
):
    tag_set = set(tags.split(",")) if tags else None
    tasks = repo.filter_tasks(tags=tag_set, completed=completed, project_id=project_id)
    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            is_completed=task.is_completed,
            tags=list(task.tags),
            project_id=task.project_id
        ) for task in tasks
    ]


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
        task_id: int,
        update_data: TaskUpdate,
        repo: InMemoryTaskRepository = Depends(get_task_repository)
):
    try:
        task = repo.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if update_data.title is not None:
            task.update_title(update_data.title)

        if update_data.is_completed is not None:
            task.is_completed = update_data.is_completed
            status = "completed" if update_data.is_completed else "incomplete"
            task._add_history(f"Marked as {status}")

        if update_data.tags is not None:
            task.tags = set(update_data.tags)
            task._add_history(f"Tags updated: {', '.join(update_data.tags)}")

        updated_task = repo.update(task_id, task)
        if not updated_task:
            raise HTTPException(status_code=500, detail="Failed to update task")

        return TaskResponse(
            id=updated_task.id,
            title=updated_task.title,
            is_completed=updated_task.is_completed,
            tags=list(updated_task.tags),
            project_id=updated_task.project_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{task_id}", status_code=204)
def delete_task(
        task_id: int,
        repo: InMemoryTaskRepository = Depends(get_task_repository)
):
    # Проверяем существование задачи перед удалением
    if not repo.get(task_id):
        raise HTTPException(status_code=404, detail="Task not found")

    if not repo.delete(task_id):
        raise HTTPException(status_code=500, detail="Failed to delete task")

    return