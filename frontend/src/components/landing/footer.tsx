import Link from "next/link";

interface FooterProps {
  data: {
    columns: {
      title: string;
      links: { text: string; href: string }[];
    }[];
    bottomText: string;
  };
}

export function Footer({ data }: FooterProps) {
  return (
    <footer className="py-16 border-t bg-muted/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          {/* Brand column */}
          <div className="lg:col-span-1">
            <Link href="/" className="flex items-center gap-2 font-bold text-xl mb-3">
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center text-white text-sm font-bold"
                style={{ backgroundColor: "#EC4899" }}
              >
                R
              </div>
              <span>DClaw Recruit</span>
            </Link>
            <p className="text-sm text-muted-foreground leading-relaxed">
              AI-powered talent acquisition platform. Hire smarter, faster, and
              more equitably.
            </p>
          </div>

          {/* Link columns */}
          {data.columns.map((col) => (
            <div key={col.title}>
              <h4 className="font-semibold text-sm mb-4">{col.title}</h4>
              <ul className="space-y-3">
                {col.links.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {link.text}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 pt-8 border-t text-center text-sm text-muted-foreground">
          {data.bottomText}
        </div>
      </div>
    </footer>
  );
}
