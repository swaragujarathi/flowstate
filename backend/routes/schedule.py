from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models import User, Task, StudySession
from schemas import SchedulePreviewItem, DailyScheduleItem
from auth import get_current_user
from services.scheduler import get_priority_weight, session_exists_today

router = APIRouter(
    tags=["Schedule"]
)

@router.get(
    "/schedule/preview",
    response_model=list[SchedulePreviewItem]
)
def get_schedule_preview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.is_completed == False
    ).all()

    today = datetime.utcnow()

    schedule = []

    for task in tasks:

        priority_weight = get_priority_weight(
        task.priority
        )

        if not task.deadline:
            continue

        remaining_hours = (
            task.estimated_hours -
            task.completed_hours
        )

        days_left = (
            task.deadline - today
        ).days

        days_left = max(days_left, 1)

        required_hours_per_day = (
            remaining_hours / days_left
        )

        urgency_score = (
            required_hours_per_day * priority_weight
        )

        schedule.append(
        {
            "task_id": task.id,

            "title": task.title,

            "priority": task.priority,

            "remaining_hours": remaining_hours,

            "days_left": days_left,

            "required_hours_per_day": round(
                required_hours_per_day,
                2
            ),

            "urgency_score": round(
                urgency_score,
                2
            ),

            "deadline": task.deadline
        }
    )
        
    schedule.sort(
        key=lambda task: task["urgency_score"],
        reverse=True
    )

    return schedule

@router.get(
    "/schedule/daily",
    response_model=list[DailyScheduleItem]
)
def generate_daily_schedule(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.is_completed == False
    ).all()

    available_hours_today = (
        current_user.daily_study_hours
    )

    today = datetime.utcnow()

    deadline_tasks = []
    no_deadline_tasks = []

    for task in tasks:

        if task.deadline:
            deadline_tasks.append(task)
        else:
            no_deadline_tasks.append(task)

    required_schedule = []

    total_required_hours = 0

    # Calculate required hours/day

    for task in deadline_tasks:

        remaining_hours = (
            task.estimated_hours -
            task.completed_hours
        )

        if remaining_hours <= 0:
            continue

        days_left = max(
            (task.deadline - today).days,
            1
        )

        required_hours_per_day = (
            remaining_hours /
            days_left
        )

        total_required_hours += (
            required_hours_per_day
        )

        required_schedule.append(
            {
                "task_id": task.id,
                "title": task.title,
                "priority": task.priority,
                "required_hours": required_hours_per_day
            }
        )

    daily_schedule = []

    # CASE 1
    # Schedule fits

    if total_required_hours <= available_hours_today:

        for item in required_schedule:

            daily_schedule.append(
                {
                    "task_id": item["task_id"],
                    "title": item["title"],
                    "priority": item["priority"],
                    "hours_today": round(
                        item["required_hours"],
                        2
                    )
                }
            )

        remaining_capacity = (
            available_hours_today -
            total_required_hours
        )

    # CASE 2
    # Overloaded
    # Compression acc. to priority

    else:

        weighted_total = 0

        for item in required_schedule:

            weight = get_priority_weight(
                item["priority"]
            )

            weighted_total += (
                item["required_hours"] * weight
            )

        for item in required_schedule:

            weight = get_priority_weight(
                item["priority"]
            )

            weighted_requirement = (
                item["required_hours"] * weight
            )

            compressed_hours = (
                weighted_requirement /
                weighted_total
            ) * available_hours_today

            daily_schedule.append(
                {
                    "task_id": item["task_id"],
                    "title": item["title"],
                    "priority": item["priority"],
                    "hours_today": round(
                        compressed_hours,
                        2
                    )
                }
            )

        remaining_capacity = 0

       # Use spare capacity

    if remaining_capacity > 0:

        # Case A:
        # Non-deadline tasks exist

        if no_deadline_tasks:

            no_deadline_tasks.sort(
                key=lambda task:
                get_priority_weight(
                    task.priority
                ),
                reverse=True
            )

            total_weight = sum(
                get_priority_weight(
                    task.priority
                )
                for task in no_deadline_tasks
            )

            for task in no_deadline_tasks:

                weight = (
                    get_priority_weight(
                        task.priority
                    )
                )

                extra_hours = (
                    weight /
                    total_weight
                ) * remaining_capacity

                daily_schedule.append(
                    {
                        "task_id": task.id,
                        "title": task.title,
                        "priority": task.priority,
                        "hours_today": round(
                            extra_hours,
                            2
                        )
                    }
                )

        # Case B:
        # No non-deadline tasks
        # Give spare time to deadline tasks by priority

        else:

            total_weight = sum(
                get_priority_weight(
                    item["priority"]
                )
                for item in required_schedule
            )

            for schedule_item in daily_schedule:

                weight = (
                    get_priority_weight(
                        schedule_item["priority"]
                    )
                )

                bonus_hours = (
                    weight /
                    total_weight
                ) * remaining_capacity

                schedule_item["hours_today"] = round(
                    schedule_item["hours_today"] +
                    bonus_hours,
                    2
                )

    # Sort final output

    daily_schedule.sort(
        key=lambda item:
        get_priority_weight(
            item["priority"]
        ),
        reverse=True
    )

    # Create Study Sessions

    for item in daily_schedule:

        if not session_exists_today(
            db,
            item["task_id"],
            current_user.id
        ):

            session = StudySession(
                task_id=item["task_id"],
                user_id=current_user.id,
                session_date=datetime.utcnow(),
                planned_hours=item["hours_today"]
            )

            db.add(session)

    db.commit()

    return daily_schedule