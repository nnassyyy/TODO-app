from fastapi import APIRouter, HTTPException, Depends
from src.repositories.project_repository import InMemoryProjectRepository
from src.repositories.task_repository import InMemoryTaskRepository
from src.schemas.project import ProjectCreate, ProjectResponse
from src.schemas.task import TaskResponse
from src.domain.project import Project
from .dependencies import get_project_repository, get_task_repository

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    repo: InMemoryProjectRepository = Depends(get_project_repository)
):
    project = Project(project_data.title, project_data.description)
    created_project = repo.create(project)
    return ProjectResponse(
        id=created_project.id,
        title=created_project.title,
        description=created_project.description,
        is_active=created_project.is_active
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    repo: InMemoryProjectRepository = Depends(get_project_repository)
):
    project = repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        is_active=project.is_active
    )


@router.get("", response_model=list[ProjectResponse])
def get_projects(
        repo: InMemoryProjectRepository = Depends(get_project_repository)
):
    projects = repo.get_active()
    return [
        ProjectResponse(
            id=project.id,
            title=project.title,
            description=project.description,
            is_active=project.is_active
        ) for project in projects
    ]


@router.get("/{project_id}/tasks", response_model=list[TaskResponse])
def get_project_tasks(
        project_id: int,
        project_repo: InMemoryProjectRepository = Depends(get_project_repository),
        task_repo: InMemoryTaskRepository = Depends(get_task_repository)
):
    if not project_repo.get(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = task_repo.filter_tasks(project_id=project_id)
    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            is_completed=task.is_completed,
            tags=list(task.tags),
            project_id=task.project_id
        ) for task in tasks
    ]