import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import GlassCard from "../components/GlassCard";

import {
  getDailySchedule,
  type DailySchedule,
} from "../api/schedule";
import { toast } from "sonner";

export default function Schedule() {
  const [schedule, setSchedule] =
    useState<DailySchedule[]>([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const data =
          await getDailySchedule();

        setSchedule(data);
      } catch (error) {
        console.error(error);
        toast.error(
            "Failed to load Schedule"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchSchedule();
  }, []);

  const totalHours =
    schedule.reduce(
      (sum, task) =>
        sum + task.hours_today,
      0
    );

  const highPriorityTasks =
    schedule.filter(
      (task) =>
        task.priority === "High"
    ).length;

  return (
    <DashboardLayout>

      <h1 className="mb-8 text-4xl font-bold">
        Today's Schedule
      </h1>

      <div className="mb-8 grid grid-cols-1 md:grid-cols-3 gap-6">

        <GlassCard className="p-6">
          <p className="text-slate-400">
            Planned Hours
          </p>

          <h2 className="mt-2 text-3xl font-bold">
            {totalHours}
          </h2>
        </GlassCard>

        <GlassCard className="p-6">
          <p className="text-slate-400">
            Tasks Today
          </p>

          <h2 className="mt-2 text-3xl font-bold">
            {schedule.length}
          </h2>
        </GlassCard>

        <GlassCard className="p-6">
          <p className="text-slate-400">
            High Priority
          </p>

          <h2 className="mt-2 text-3xl font-bold">
            {highPriorityTasks}
          </h2>
        </GlassCard>

      </div>

      {loading ? (
        <p>Loading...</p>
      ) : schedule.length === 0 ? (
        <GlassCard className="p-8 text-center">
            <h3 className="text-xl font-semibold">
            No Schedule Generated
            </h3>

            <p className="mt-2 text-slate-400">
            Create some tasks and FlowState
            will automatically build your study
            schedule.
            </p>
        </GlassCard>
        ) : (
        <div className="space-y-4">

          {schedule.map((task) => (
            <GlassCard
              key={task.task_id}
              className="p-6"
            >
              <h3 className="text-xl font-semibold">
                {task.title}
              </h3>

              <div className="mt-3 flex gap-6 text-sm text-slate-400">

                <span>
                  Priority:
                  {" "}
                  {task.priority}
                </span>

                <span>
                  Hours Today:
                  {" "}
                  {task.hours_today}
                </span>

              </div>
            </GlassCard>
          ))}

        </div>
      )}

    </DashboardLayout>
  );
}