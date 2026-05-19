interface HowItWorksProps {
  data: {
    heading: string;
    steps: {
      number: number;
      title: string;
      description: string;
    }[];
  };
}

export function HowItWorks({ data }: HowItWorksProps) {
  return (
    <section id="how-it-works" className="py-20 lg:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-center mb-16">
          {data.heading}
        </h2>

        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {data.steps.map((step) => (
            <div key={step.number} className="relative text-center group">
              {/* Connector line */}
              {step.number < data.steps.length && (
                <div className="hidden lg:block absolute top-8 left-[60%] w-[80%] h-0.5 bg-gradient-to-r from-pink-200 to-pink-100 dark:from-pink-800 dark:to-pink-900" />
              )}

              {/* Step number */}
              <div className="w-16 h-16 rounded-2xl bg-pink-50 dark:bg-pink-950/50 border-2 border-pink-200 dark:border-pink-800 flex items-center justify-center mx-auto mb-4 group-hover:bg-pink-100 dark:group-hover:bg-pink-900/50 group-hover:scale-110 transition-all duration-300">
                <span className="text-2xl font-bold text-pink-600 dark:text-pink-400">
                  {step.number}
                </span>
              </div>

              <h3 className="text-lg font-semibold mb-2">{step.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
