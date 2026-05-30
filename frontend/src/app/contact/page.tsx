"use client";

import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Zap, Loader2, CheckCircle2, Mail, MessageSquare, Building2 } from "lucide-react";

export default function ContactPage() {
  const [loading, setLoading] = React.useState(false);
  const [sent, setSent] = React.useState(false);
  const [form, setForm] = React.useState({ name: "", email: "", company: "", role: "", message: "" });

  function set(k: string, v: string) { setForm((f) => ({ ...f, [k]: v })); }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1000));
    setLoading(false);
    setSent(true);
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <nav className="border-b border-border/50 bg-background/90 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 font-bold">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center">
              <Zap className="h-3.5 w-3.5 text-white" />
            </div>
            <span className="text-sm bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
              DClaw Recruit
            </span>
          </Link>
          <Link href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            ← Back to home
          </Link>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid lg:grid-cols-2 gap-16 items-start">
          {/* Left: copy */}
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-pink-950/50 border border-pink-800/50 text-xs text-pink-300 mb-6">
              Enterprise Sales
            </div>
            <h1 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
              Talk to our team
            </h1>
            <p className="text-muted-foreground text-lg mb-8 leading-relaxed">
              See how DClaw Recruit can transform your hiring process. We&apos;ll walk you through AI sourcing, screening, and analytics tailored to your team.
            </p>

            <div className="space-y-5">
              {[
                { icon: Building2, title: "Enterprise & Startup Plans", desc: "Custom pricing for 5 to 5,000 employees" },
                { icon: MessageSquare, title: "Live Demo", desc: "30-minute walkthrough of the full platform" },
                { icon: Mail, title: "Response in < 1 business day", desc: "Guaranteed reply from a human" },
              ].map((item) => (
                <div key={item.title} className="flex gap-4">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-pink-950/60 to-purple-950/40 border border-pink-800/30 flex items-center justify-center shrink-0">
                    <item.icon className="h-4 w-4 text-pink-400" />
                  </div>
                  <div>
                    <div className="font-semibold text-sm text-foreground">{item.title}</div>
                    <div className="text-xs text-muted-foreground mt-0.5">{item.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right: form */}
          <div className="bg-card/40 border border-border/50 rounded-2xl p-8">
            {sent ? (
              <div className="text-center py-8">
                <CheckCircle2 className="h-12 w-12 text-emerald-400 mx-auto mb-4" />
                <h2 className="text-xl font-bold text-foreground mb-2">Message received!</h2>
                <p className="text-sm text-muted-foreground mb-6">
                  We&apos;ll be in touch within 1 business day.
                </p>
                <Button size="sm" variant="outline" onClick={() => setSent(false)} className="border-border/50 text-xs">
                  Send another message
                </Button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <h2 className="font-semibold text-base text-foreground mb-4">Get in touch</h2>
                <div className="grid sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <Label className="text-xs text-muted-foreground">Full Name *</Label>
                    <Input
                      placeholder="Sarah Chen"
                      value={form.name}
                      onChange={(e) => set("name", e.target.value)}
                      className="bg-muted/30 border-border/50 h-9 text-sm"
                      required
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label className="text-xs text-muted-foreground">Work Email *</Label>
                    <Input
                      type="email"
                      placeholder="sarah@acme.com"
                      value={form.email}
                      onChange={(e) => set("email", e.target.value)}
                      className="bg-muted/30 border-border/50 h-9 text-sm"
                      required
                    />
                  </div>
                </div>
                <div className="grid sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <Label className="text-xs text-muted-foreground">Company</Label>
                    <Input
                      placeholder="Acme Inc."
                      value={form.company}
                      onChange={(e) => set("company", e.target.value)}
                      className="bg-muted/30 border-border/50 h-9 text-sm"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label className="text-xs text-muted-foreground">Your Role</Label>
                    <Input
                      placeholder="Head of Talent"
                      value={form.role}
                      onChange={(e) => set("role", e.target.value)}
                      className="bg-muted/30 border-border/50 h-9 text-sm"
                    />
                  </div>
                </div>
                <div className="space-y-1.5">
                  <Label className="text-xs text-muted-foreground">How can we help?</Label>
                  <textarea
                    rows={4}
                    placeholder="Tell us about your hiring challenges, team size, and what you're looking for..."
                    value={form.message}
                    onChange={(e) => set("message", e.target.value)}
                    className="w-full rounded-md border border-border/50 bg-muted/30 px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-1 focus:ring-pink-600 resize-none"
                  />
                </div>
                <Button
                  type="submit"
                  disabled={loading}
                  className="w-full h-10 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white border-0 rounded-xl text-sm font-medium"
                >
                  {loading ? <><Loader2 className="h-4 w-4 animate-spin mr-2" />Sending...</> : "Send Message"}
                </Button>
              </form>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
