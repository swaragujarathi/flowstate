import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { registerUser } from "../api/auth";

export default function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] =
    useState("");
  const [confirmPassword, setConfirmPassword] =
    useState("");

  const [dailyStudyHours, setDailyStudyHours] =
    useState(5);

  const [error, setError] = useState("");
  const [loading, setLoading] =
    useState(false);

  const handleRegister = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    setError("");

    if (password.length < 8) {
      setError(
        "Password must be at least 8 characters long"
      );
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      setLoading(true);

      await registerUser(
        name,
        email,
        password,
        dailyStudyHours
      );

      toast.success(
        "Account created successfully"
      );

      navigate("/login");
    } catch (err: any) {
      toast.error("Registration failed");

      const detail =
        err?.response?.data?.detail;

      if (typeof detail === "string") {
        setError(detail);
      } else if (
        Array.isArray(detail)
      ) {
        setError(
          detail[0]?.msg ||
          "Registration failed"
        );
      } else {
        setError(
          "Registration failed"
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="
        min-h-screen
        bg-[#0A0A0A]
        flex
        items-center
        justify-center
        px-4
      "
    >
      <div
        className="
          w-full
          max-w-md
          rounded-3xl
          border
          border-white/10
          bg-white/5
          backdrop-blur-xl
          p-8
        "
      >
        <h1
          className="
            text-3xl
            font-bold
            text-center
            mb-2
          "
        >
          Create Account
        </h1>

        <p
          className="
            text-slate-400
            text-center
            mb-8
          "
        >
          Join FlowState
        </p>

        {error && (
          <div
            className="
              mb-4
              rounded-xl
              bg-red-500/10
              border
              border-red-500/20
              p-3
              text-red-400
            "
          >
            {error}
          </div>
        )}

        <form
          onSubmit={handleRegister}
          className="space-y-4"
        >
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) =>
              setName(e.target.value)
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
            required
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
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
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
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
            required
          />

          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) =>
              setConfirmPassword(
                e.target.value
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
            required
          />

          <div className="text-center">
            <label
              className="
                mb-3
                block
                text-center
                text-sm
                font-medium
                text-slate-300
              "
            >
              How many hours can you realistically study each day?
            </label>

            <input
              type="number"
              placeholder="5"
              value={dailyStudyHours}
              onChange={(e) =>
                setDailyStudyHours(
                  Number(e.target.value)
                )
              }
              min="1"
              max="24"
              className="
                text-center
                w-full
                rounded-xl
                border
                border-white/10
                bg-white/5
                px-4
                py-3
              "
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="
              w-full
              rounded-xl
              bg-purple-600
              py-3
              font-semibold
              hover:bg-purple-500
              transition
            "
          >
            {loading
              ? "Creating Account..."
              : "Create Account"}
          </button>
        </form>

        <p
          className="
            mt-6
            text-center
            text-slate-400
          "
        >
          Already have an account?{" "}
          <Link
            to="/login"
            className="
              text-purple-400
              hover:text-purple-300
            "
          >
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}