from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import User, Task
from schemas import TaskCreate, TaskResponse, ProgressUpdate, TaskStatsResponse
from auth import get_current_user

router = APIRouter(
    tags=["Tasks"]
)

@router.post(
    "/tasks",
    response_model=TaskResponse
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        estimated_hours=task.estimated_hours,
        completed_hours=0,
        deadline=task.deadline,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    tasks = (
        db.query(Task)
        .filter(Task.user_id == current_user.id)
        .all()
    )

    return tasks

@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return task

@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = (
    db.query(Task)
    .filter(Task.id == task_id)
    .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    task.title = task_data.title

    task.description = task_data.description

    task.priority = task_data.priority

    task.estimated_hours = task_data.estimated_hours

    task.deadline = task_data.deadline

    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = (
    db.query(Task)
    .filter(Task.id == task_id)
    .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(task)
    db.commit()
    return {
        "message": "Task deleted successfully"
    }

@router.patch("/tasks/{task_id}/progress",
           response_model=TaskResponse)
def update_progress(
    task_id: int,
    progress: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    if progress.completed_hours > task.estimated_hours:
        raise HTTPException(
            status_code=400,
            detail="Completed hours cannot exceed estimated hours"
        )

    task.completed_hours = progress.completed_hours
    if task.completed_hours == task.estimated_hours:
        task.is_completed = True
    else:
        task.is_completed = False

    db.commit()
    db.refresh(task)

    return task

@router.get(
    "/tasks/{task_id}/stats",
    response_model=TaskStatsResponse
)
def get_task_stats(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    remaining_hours = (
        task.estimated_hours -
        task.completed_hours
    )

    if task.estimated_hours == 0:
        completion_percentage = 0
    else:
        completion_percentage = (
            task.completed_hours /
            task.estimated_hours
        ) * 100

    return {
        "task_id": task.id,
        "title": task.title,

        "estimated_hours": task.estimated_hours,
        "completed_hours": task.completed_hours,

        "remaining_hours": remaining_hours,

        "completion_percentage": round(
            completion_percentage,
            2
        ),

        "is_completed": task.is_completed
    }