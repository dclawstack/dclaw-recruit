import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" })

export const metadata: Metadata = {
  title: "DClaw Recruit — AI-Powered Talent Acquisition",
  description:
    "Hire smarter, faster with DClaw Recruit. AI-driven sourcing, resume screening, interview scheduling, and offer management — all in one platform.",
  keywords: ["recruiting", "ATS", "AI recruiting", "hiring", "talent acquisition", "applicant tracking"],
  openGraph: {
    title: "DClaw Recruit — AI-Powered Talent Acquisition",
    description:
      "Hire smarter, faster with DClaw Recruit. AI-driven sourcing, resume screening, interview scheduling, and offer management.",
    type: "website",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="dark scroll-smooth">
      <body className={`${inter.className} ${inter.variable} antialiased`}>{children}</body>
    </html>
  )
}
