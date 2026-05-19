interface TestimonialsProps {
  data: {
    heading: string;
    items: {
      quote: string;
      author: string;
      role: string;
      avatar: string;
    }[];
  };
}

export function Testimonials({ data }: TestimonialsProps) {
  return (
    <section id="testimonials" className="py-20 lg:py-28 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-center mb-16">
          {data.heading}
        </h2>

        <div className="grid gap-8 md:grid-cols-3">
          {data.items.map((item) => (
            <div
              key={item.author}
              className="bg-card border rounded-xl p-6 flex flex-col"
            >
              {/* Quote */}
              <blockquote className="flex-1">
                <svg
                  className="h-8 w-8 text-pink-200 dark:text-pink-800 mb-3"
                  fill="currentColor"
                  viewBox="0 0 32 32"
                >
                  <path d="M9.352 4C4.456 7.456 1 13.12 1 19.36c0 5.088 3.072 8.064 6.624 8.064 3.36 0 5.856-2.688 5.856-5.856 0-3.168-2.208-5.472-5.088-5.472-.576 0-1.344.096-1.536.192.48-3.264 3.552-7.104 6.624-9.024L9.352 4zm16.512 0c-4.8 3.456-8.256 9.12-8.256 15.36 0 5.088 3.072 8.064 6.624 8.064 3.264 0 5.856-2.688 5.856-5.856 0-3.168-2.304-5.472-5.184-5.472-.576 0-1.248.096-1.44.192.48-3.264 3.456-7.104 6.528-9.024L25.864 4z" />
                </svg>
                <p className="text-muted-foreground leading-relaxed text-sm">
                  {item.quote}
                </p>
              </blockquote>

              {/* Author */}
              <div className="flex items-center gap-3 mt-6 pt-4 border-t">
                <div className="w-10 h-10 rounded-full bg-pink-100 dark:bg-pink-900/50 flex items-center justify-center text-pink-600 dark:text-pink-400 font-semibold text-sm">
                  {item.author
                    .split(" ")
                    .map((n) => n[0])
                    .join("")}
                </div>
                <div>
                  <div className="font-semibold text-sm">{item.author}</div>
                  <div className="text-xs text-muted-foreground">
                    {item.role}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
