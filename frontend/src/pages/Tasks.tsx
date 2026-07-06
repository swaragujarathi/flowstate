import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import GlassCard from "../components/GlassCard";
import { toast } from "sonner";
import {
  getTasks,
  createTask,
  deleteTask,
  updateTask
} from "../api/tasks";
import api from "../api/axios";

interface Task {
  id: number;
  title: string;
  description: string;
  priority: string;
  estimated_hours: number;
  completed_hours: number;
  is_completed: boolean;
  deadline: string;
}

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [aiPrompt, setAiPrompt] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [generatedTasks, setGeneratedTasks] =
    useState<any[]>([]);

  const [title, setTitle] = useState("");
  const [description, setDescription] =
    useState("");

  const [priority, setPriority] =
    useState("Medium");

  const [estimatedHours, setEstimatedHours] =
    useState<number | "">("");

  const [deadline, setDeadline] =
    useState("");

  const fetchTasks = async () => {
    try {
      const data = await getTasks();
      setTasks(data);
    } catch (error) {
      console.error(error);
      toast.error(
        "Failed to load tasks"
      );
    } finally {
      setLoading(false);
    }
  };

  const [editingTask, setEditingTask] = useState<any>(null);

  const [editForm, setEditForm] = useState({
    title: "",
    description: "",
    priority: "Medium",
    estimated_hours: 1,
    deadline: "",
  });

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleCreateTask = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    try {
      await createTask({
        title,
        description,
        priority,
        estimated_hours: estimatedHours,
        deadline,
      });
      toast.success("Task created successfully");
      setTitle("");
      setDescription("");
      setPriority("Medium");
      setEstimatedHours(1);
      setDeadline("");

      fetchTasks();
    } catch (error) {
      console.error(error);
      toast.error(
          "Failed to create task"
      );
    }
  };

  const handleDelete = async (
    id: number
    ) => {
    if (
        !window.confirm(
        "Delete this task?"
        )
    ) {
        return;
    }

    try {
        await deleteTask(id);

        toast.success("Task deleted");

        setTasks((prev) =>
        prev.filter(
            (task) => task.id !== id
        )
        );
    } catch (error) {
        console.error(error);

        toast.error(
        "Failed to delete task"
        );
    }
    };

  const handleEditClick = (task: Task) => {
    setEditingTask(task);

    setEditForm({
        title: task.title,
        description: task.description,
        priority: task.priority,
        estimated_hours: task.estimated_hours,
        deadline: task.deadline.slice(0, 16),
    });
  };

  const handleUpdateTask = async () => {
    if (!editingTask) return;

    try {
        await updateTask(
        editingTask.id,
        {
            ...editForm,
            estimated_hours: Number(
            editForm.estimated_hours
            ),
        }
        );
        toast.success("Task updated");
        await fetchTasks();

        setEditingTask(null);
    } catch (error) {
        console.error(error);
        toast.error(
            "Failed to update task"
        );
    }
  };

  const handleGenerateAI = async () => {
      if (!aiPrompt.trim()) {
          toast.error("Enter your study plan.");
          return;
      }

      setAiLoading(true);

      try {

          const res = await api.post(
              "/ai/parse",
              {
                  text: aiPrompt
              }
          );

          setGeneratedTasks(res.data.tasks);

          toast.success("Tasks generated!");

      } catch (err) {

          console.error(err);

          toast.error("Failed to generate tasks.");

      } finally {

          setAiLoading(false);

      }
  };

  const handleSaveGeneratedTasks = async () => {
    try {
      for (const task of generatedTasks) {
        await createTask({
          title: task.title,
          description: "",
          priority: task.priority,
          estimated_hours: task.estimated_hours,
          deadline: task.deadline,
        });
      }

      toast.success("Tasks added successfully!");

      setGeneratedTasks([]);
      setAiPrompt("");

      fetchTasks();

    } catch (error) {
      toast.error("Failed to save tasks.");
    }
  };

  const updateGeneratedTask = (
    index: number,
    field: keyof AITask,
    value: AITask[keyof AITask]
  ) => {
    const updated = [...generatedTasks];

    updated[index] = {
      ...updated[index],
      [field]: value,
    };

    setGeneratedTasks(updated);
  };

  return (
    <DashboardLayout>

      <h1 className="mb-8 text-4xl font-bold">
        Tasks
      </h1>

      <GlassCard className="mb-8 p-6">

        <h2 className="mb-4 text-xl font-semibold">
          Create Task
        </h2>

        <form
          onSubmit={handleCreateTask}
          className="space-y-4"
        >

          <input
            type="text"
            placeholder="Task Title"
            value={title}
            onChange={(e) =>
              setTitle(e.target.value)
            }
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3"
          />

          <textarea
            placeholder="Description"
            value={description}
            onChange={(e) =>
              setDescription(
                e.target.value
              )
            }
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3"
          />

          <select
            value={priority}
            onChange={(e) =>
              setPriority(
                e.target.value
              )
            }
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3"
          >
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
          </select>

          <input
            type="number"
            min="1"
            placeholder="Estimated Hours"
            value={estimatedHours}
            onChange={(e) =>
                setEstimatedHours(
                    e.target.value === ""
                    ? ""
                    : Number(e.target.value)
                )
            }
            className="
                w-full
                rounded-xl
                border
                border-white/10
                bg-white/5
                px-4
                py-3
            "
          />

          <input
            type="datetime-local"
            value={deadline}
            onChange={(e) =>
              setDeadline(
                e.target.value
              )
            }
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3"
          />

          <button
            type="submit"
            className="
              rounded-xl
              bg-purple-600
              px-6
              py-3
              font-semibold
              hover:bg-purple-500
            "
          >
            Create Task
          </button>

        </form>

      </GlassCard>

      <GlassCard className="mb-8 p-6">

        <h2 className="mb-2 text-xl font-semibold">
          ✨ Generate Tasks with AI
        </h2>

        <p className="mb-4 text-slate-400">
          Describe your study plan and let AI create tasks for you.
        </p>

        <textarea
          rows={5}
          value={aiPrompt}
          onChange={(e) => setAiPrompt(e.target.value)}
          placeholder={
          `Example:
          I have my DSA exam on July 20.
          Finish Graphs in 10 hours.
          Finish Dynamic Programming in 15 hours.
          Revise SQL in 5 hours.`}
          className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3"
        />

        <button
          onClick={handleGenerateAI}
          disabled={aiLoading}
          className="mt-4 rounded-xl bg-purple-600 px-6 py-3 font-semibold hover:bg-purple-500 disabled:opacity-50"
        >
          {aiLoading ? "Generating..." : "Generate Tasks"}
        </button>

      </GlassCard>

      {
        generatedTasks.length > 0 && (

        <GlassCard className="mb-8 p-6">

        <h2 className="mb-4 text-xl font-semibold">
        Generated Tasks
        </h2>

        <div className="space-y-4">

        {generatedTasks.map((task, index) => (

            <div
              key={index}
              className="rounded-xl border border-white/10 bg-white/5 p-5 space-y-4"
            >

              <div>
                <label className="mb-1 block text-sm text-slate-400">
                  Title
                </label>

                <input
                  type="text"
                  value={task.title}
                  onChange={(e) =>
                    updateGeneratedTask(index, "title", e.target.value)
                  }
                  className="w-full rounded-xl border border-white/10 bg-slate-800 px-4 py-2"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm text-slate-400">
                  Estimated Hours
                </label>

                <input
                  type="number"
                  min="1"
                  value={task.estimated_hours}
                  onChange={(e) =>
                    updateGeneratedTask(
                      index,
                      "estimated_hours",
                      Number(e.target.value)
                    )
                  }
                  className="w-full rounded-xl border border-white/10 bg-slate-800 px-4 py-2"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm text-slate-400">
                  Priority
                </label>

                <select
                  value={task.priority}
                  onChange={(e) =>
                    updateGeneratedTask(index, "priority", e.target.value)
                  }
                  className="w-full rounded-xl border border-white/10 bg-slate-800 px-4 py-2"
                >
                  <option>High</option>
                  <option>Medium</option>
                  <option>Low</option>
                </select>
              </div>

              <div>
                <label className="mb-1 block text-sm text-slate-400">
                  Difficulty
                </label>

                <select
                  value={task.difficulty}
                  onChange={(e) =>
                    updateGeneratedTask(index, "difficulty", e.target.value)
                  }
                  className="w-full rounded-xl border border-white/10 bg-slate-800 px-4 py-2"
                >
                  <option>Easy</option>
                  <option>Medium</option>
                  <option>Hard</option>
                </select>
              </div>

              <div>
                <label className="mb-1 block text-sm text-slate-400">
                  Deadline
                </label>

                <input
                  type="date"
                  value={task.deadline ?? ""}
                  onChange={(e) =>
                    updateGeneratedTask(index, "deadline", e.target.value)
                  }
                  className="w-full rounded-xl border border-white/10 bg-slate-800 px-4 py-2"
                />
              </div>

              <button
                onClick={() => {
                  setGeneratedTasks(
                    generatedTasks.filter((_, i) => i !== index)
                  );
                }}
                className="rounded-lg bg-red-500/20 px-4 py-2 text-red-400 hover:bg-red-500/30"
              >
                Remove Task
              </button>

            </div>

          ))}

        </div>

        <button
          onClick={handleSaveGeneratedTasks}
          className="mt-6 rounded-xl bg-green-600 px-6 py-3 font-semibold hover:bg-green-500"
        >
          Save All
        </button>

        </GlassCard>

        )
      }

      <div className="space-y-4">

        {loading ? (
          <p>Loading...</p>
        ) : tasks.length === 0 ? (
            <GlassCard className="p-8 text-center">
                <h3 className="text-xl font-semibold">
                No Tasks Yet
                </h3>

                <p className="mt-2 text-slate-400">
                Create your first task to get started.
                </p>
            </GlassCard>
        ) : (
          tasks.map((task) => {
            const progress =
                task.estimated_hours > 0
                ? Math.min(
                    (task.completed_hours /
                        task.estimated_hours) *
                        100,
                    100
                    )
                : 0;

            return (
                <GlassCard
                key={task.id}
                className="p-6"
                >
                <div className="flex items-start justify-between">

                    <div className="flex-1">

                    <div className="flex items-center gap-3">
                        <h3 className="text-xl font-semibold">
                        {task.title}
                        </h3>

                        {task.is_completed && (
                        <span className="rounded-full bg-green-500/20 px-2 py-1 text-xs text-green-400">
                            Completed
                        </span>
                        )}
                    </div>

                    <p className="mt-2 text-slate-400">
                        {task.description}
                    </p>

                    <p className="mt-2 text-sm text-purple-400">
                        Deadline{" "}
                        {new Date(
                        task.deadline
                        ).toLocaleDateString()}
                    </p>

                    <div className="mt-4 flex gap-6 text-sm text-slate-400">

                        <span>
                        Priority: {task.priority}
                        </span>

                        <span>
                        {task.completed_hours}
                        /
                        {task.estimated_hours}
                        hrs
                        </span>

                        <span
                        className={
                            task.is_completed
                            ? "text-green-400"
                            : "text-yellow-400"
                        }
                        >
                        {task.is_completed
                            ? "Completed"
                            : "Pending"}
                        </span>

                    </div>

                    <div className="mt-4">

                        <div className="mb-2 flex justify-between text-sm">

                        <span className="text-slate-400">
                            Progress
                        </span>

                        <span className="text-purple-400">
                            {Math.round(progress)}%
                        </span>

                        </div>

                        <div className="h-2 w-full overflow-hidden rounded-full bg-slate-700">

                        <div
                            className={`h-full transition-all duration-500 ${
                            task.is_completed
                                ? "bg-green-500"
                                : "bg-purple-500"
                            }`}
                            style={{
                            width: `${progress}%`,
                            }}
                        />

                        </div>

                    </div>

                    </div>

                    <div className="ml-6 flex gap-2">

                    <button
                        onClick={() =>
                        handleEditClick(task)
                        }
                        className="
                        rounded-lg
                        bg-cyan-500/20
                        px-4
                        py-2
                        text-cyan-400
                        "
                    >
                        Edit
                    </button>

                    <button
                        onClick={() =>
                        handleDelete(task.id)
                        }
                        className="
                        rounded-lg
                        bg-red-500/20
                        px-4
                        py-2
                        text-red-400
                        "
                    >
                        Delete
                    </button>

                    </div>

                </div>
                </GlassCard>
            );
            })
        )}

      </div>

      {editingTask && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
            <div className="w-full max-w-lg rounded-2xl border border-white/10 bg-slate-900 p-6">

            <h2 className="mb-4 text-xl font-semibold">
                Edit Task
            </h2>

            <div className="space-y-4">

            <input
            type="text"
            value={editForm.title}
            onChange={(e) =>
                setEditForm({
                ...editForm,
                title: e.target.value,
                })
            }
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3"
            />

            <textarea
            value={editForm.description}
            onChange={(e) =>
                setEditForm({
                ...editForm,
                description: e.target.value,
                })
            }
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3"
            />

            <select
                value={editForm.priority}
                onChange={(e) =>
                    setEditForm({
                    ...editForm,
                    priority: e.target.value,
                    })
                }
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3"
            >
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
            </select>

            <input
            type="number"
            value={editForm.estimated_hours}
            onChange={(e) =>
                setEditForm({
                ...editForm,
                estimated_hours: Number(
                    e.target.value
                ),
                })
            }
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3"
            />

            <input
            type="datetime-local"
            value={editForm.deadline}
            onChange={(e) =>
                setEditForm({
                ...editForm,
                deadline: e.target.value,
                })
            }
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3"
            />

            <div className="flex gap-3">

            <button
                onClick={handleUpdateTask}
                className="rounded-xl bg-purple-600 px-5 py-2"
            >
                Save
            </button>

            <button
                onClick={() =>
                setEditingTask(null)
                }
                className="rounded-xl bg-slate-700 px-5 py-2"
            >
                Cancel
            </button>

        </div>

      </div>

    </div>
  </div>
)}

    </DashboardLayout>
);
}