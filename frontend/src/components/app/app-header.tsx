"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Plus, Bell } from "lucide-react";

interface AppHeaderProps {
  title: string;
  action?: { label: string; href: string };
}

export function AppHeader({ title, action }: AppHeaderProps) {
  return (
    <header className="h-16 border-b border-border/50 flex items-center justify-between px-6 bg-background/80 backdrop-blur-sm sticky top-0 z-40">
      <h1 className="text-lg font-semibold text-foreground">{title}</h1>
      <div className="flex items-center gap-3">
        <button className="relative p-2 rounded-lg hover:bg-muted/50 transition-colors text-muted-foreground hover:text-foreground">
          <Bell className="h-4 w-4" />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-pink-500" />
        </button>
        {action && (
          <Button
            size="sm"
            className="bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white border-0 rounded-lg h-8 px-3 text-xs"
            asChild
          >
            <Link href={action.href} className="flex items-center gap-1.5">
              <Plus className="h-3.5 w-3.5" />
              {action.label}
            </Link>
          </Button>
        )}
      </div>
    </header>
  );
}
