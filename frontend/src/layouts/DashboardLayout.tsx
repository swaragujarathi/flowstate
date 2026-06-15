import { useState } from "react";
import Sidebar from "../components/Sidebar";

type Props = {
  children: React.ReactNode;
};

export default function DashboardLayout({
  children,
}: Props) {
  const [sidebarOpen, setSidebarOpen] =
    useState(false);

  return (
    <div className="min-h-screen bg-[#0A0A0A] text-white">

      {/* Mobile Header */}

      <div className="md:hidden flex items-center justify-between p-4 border-b border-white/10">
        <h1 className="text-xl font-bold text-purple-400">
          FlowState
        </h1>

        <button
          onClick={() =>
            setSidebarOpen(!sidebarOpen)
          }
          className="text-2xl"
        >
          ☰
        </button>
      </div>

      {/* Mobile Sidebar */}

      {sidebarOpen && (
        <div className="md:hidden fixed inset-0 z-50 bg-black/50">
          <div className="w-64 h-full">
            <Sidebar />
          </div>
        </div>
      )}

      <div className="flex">

        {/* Desktop Sidebar */}

        <div className="hidden md:block">
          <Sidebar />
        </div>

        <main className="flex-1 p-4 md:p-8">
          {children}
        </main>

      </div>
    </div>
  );
}