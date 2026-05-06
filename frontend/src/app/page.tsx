import Link from "next/link";
import { UserPlus } from "lucide-react";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen px-4">
      <UserPlus className="w-16 h-16 text-brand mb-6" />
      <h1 className="text-4xl font-bold text-brand mb-4">DClaw Recruit</h1>
      <p className="text-lg text-gray-600 mb-8">Job posting, candidate ranking</p>
      <Link
        href="/dashboard"
        className="inline-flex items-center justify-center px-6 py-3 text-white bg-brand rounded-lg hover:opacity-90 transition-opacity"
      >
        Go to Dashboard
      </Link>
    </main>
  );
}
