import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import AuthLayout from "../components/AuthLayout";
import { loginUser } from "../api/auth";
import { toast } from "sonner";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError("");

      const data = await loginUser(
        email,
        password
      );

      localStorage.setItem(
        "token",
        data.access_token
      );
      toast.success("Welcome back!");
      navigate("/");
    } catch (err) {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div className="w-full max-w-md rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-xl">

        <h1 className="mb-2 text-3xl font-bold">
          Welcome Back
        </h1>

        <p className="mb-8 text-slate-400">
          Sign in to your FlowState
        </p>

        <form
          onSubmit={handleSubmit}
          className="space-y-4"
        >

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 outline-none transition focus:border-purple-500"
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 outline-none transition focus:border-purple-500"
          />

          {error && (
            <p className="text-sm text-red-400">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="
              w-full
              rounded-xl
              bg-purple-600
              py-3
              font-semibold
              transition
              hover:bg-purple-500
              disabled:opacity-50
            "
          >
            {loading
              ? "Signing In..."
              : "Login"}
          </button>

        </form>

      <p className="mt-6 text-center text-slate-400">
        Don't have an account?{" "}
        <Link
          to="/register"
          className="text-purple-400 hover:text-purple-300"
        >
          Create one
        </Link>
      </p>
      </div>
    </AuthLayout>
  );
}