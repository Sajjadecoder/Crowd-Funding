import Navbar from "@/components/Navbar"

const categories = ["Technology", "Art", "Education", "Health", "Social Causes", "Environment", "Music", "Film"]

const featuredCampaigns = [
  { id: 1, title: "Smart Eco Bottle", category: "Technology", raised: 24000, goal: 40000 },
  { id: 2, title: "Community Art Wall", category: "Art", raised: 12000, goal: 15000 },
  { id: 3, title: "STEM Kits for Schools", category: "Education", raised: 7600, goal: 12000 },
  { id: 4, title: "Rural Health Van", category: "Health", raised: 53000, goal: 80000 },
  { id: 5, title: "Beach Cleanup Drive", category: "Environment", raised: 9800, goal: 10000 },
  { id: 6, title: "Indie Film Short", category: "Film", raised: 4200, goal: 9000 },
]

const testimonials = [
  {
    id: 1,
    name: "Ava D.",
    role: "Creator",
    quote: "We hit 120% of our goal in 18 days. The backers’ support turned our idea into a real product.",
  },
  {
    id: 2,
    name: "Liam K.",
    role: "Backer",
    quote: "Supporting projects here feels personal. I love tracking progress and seeing updates roll in.",
  },
  {
    id: 3,
    name: "Noah S.",
    role: "Creator",
    quote: "The platform’s simplicity helped us focus on storytelling—and it paid off.",
  }
]

function formatCurrency(n) {
  try {
    return new Intl.NumberFormat(undefined, { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n)
  } catch {
    return `$${n.toLocaleString()}`
  }
}

export default function Home() {
  return (
    <>
      <Navbar />
      <main className="font-sans w-full text-white bg-gradient-to-br from-gray-900 via-gray-800 to-black">
        {/* Hero Section */}
        <section aria-label="Hero" className="relative w-full">
          <div className="w-full h-[52vh] md:h-[60vh] lg:h-[70vh] flex items-center justify-center text-center">
            <div className="px-6 md:px-10 max-w-4xl">
              <p className="mb-2 text-sm uppercase tracking-widest text-gray-400">
                Crowdfunding Platform
              </p>
              <h1 className="text-3xl md:text-5xl font-semibold tracking-tight">
                Support Creative Ideas. Fund the Future.
              </h1>
              <p className="mt-4 text-gray-300">
                Discover inspiring projects across technology, art, education, health, and more. 
                Back the creators you believe in and help bring bold ideas to life.
              </p>

              <div className="mt-6 flex flex-col sm:flex-row items-center gap-3 justify-center">
                <a
                  href="#featured"
                  className="inline-flex h-10 items-center justify-center rounded-md bg-indigo-600 px-5 text-sm font-medium text-white hover:bg-indigo-500 transition"
                >
                  Explore Campaigns
                </a>
                <a
                  href="#cta"
                  className="inline-flex h-10 items-center justify-center rounded-md border border-gray-600 bg-gray-800 px-5 text-sm font-medium hover:bg-gray-700 transition"
                >
                  Start a Campaign
                </a>
              </div>
            </div>
          </div>
        </section>

        {/* Categories Section */}
        <section id="categories" className="w-full px-4 md:px-6 py-10">
          <h2 className="text-xl md:text-2xl font-semibold mb-4">Browse by Category</h2>
          <div className="flex gap-2 overflow-x-auto no-scrollbar py-2">
            {categories.map((c) => (
              <button
                key={c}
                className="whitespace-nowrap rounded-full border border-gray-700 bg-gray-800 px-4 py-2 text-sm text-white hover:bg-gray-700"
                type="button"
              >
                {c}
              </button>
            ))}
          </div>
        </section>

        {/* Featured Campaigns */}
        <section id="featured" className="w-full px-4 md:px-6 pb-12">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl md:text-2xl font-semibold">Featured Campaigns</h2>
            <a href="#" className="text-sm text-gray-400 hover:text-white">View all</a>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {featuredCampaigns.map((c) => {
              const pct = Math.min(100, Math.round((c.raised / c.goal) * 100))
              return (
                <article key={c.id} className="rounded-lg border border-gray-700 bg-gray-900 p-4 flex flex-col gap-3">
                  <div className="aspect-[16/9] w-full bg-gray-800 border border-gray-700 rounded-md flex items-center justify-center text-gray-400 text-sm">
                    {"Add campaign image here"}
                  </div>

                  <span className="inline-flex items-center rounded-full bg-gray-800 px-2 py-1 text-xs text-gray-300">
                    {c.category}
                  </span>

                  <h3 className="text-base md:text-lg font-medium">{c.title}</h3>

                  <div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-medium">{formatCurrency(c.raised)}</span>
                      <span className="text-gray-400">of {formatCurrency(c.goal)}</span>
                    </div>
                    <div className="mt-2 h-2 w-full rounded-full bg-gray-800 overflow-hidden">
                      <div
                        className="h-full bg-indigo-600"
                        style={{ width: `${pct}%` }}
                        role="progressbar"
                      />
                    </div>
                    <div className="mt-1 text-xs text-gray-400">{pct}% funded</div>
                  </div>

                  <div className="mt-2 flex gap-2">
                    <a
                      href="#"
                      className="inline-flex items-center justify-center rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-sm hover:bg-gray-700"
                    >
                      Details
                    </a>
                    <a
                      href="#"
                      className="inline-flex items-center justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-500"
                    >
                      Back this
                    </a>
                  </div>
                </article>
              )
            })}
          </div>
        </section>

        {/* Testimonials */}
        <section id="testimonials" className="w-full px-4 md:px-6 py-12">
          <h2 className="text-xl md:text-2xl font-semibold text-center mb-4">Success Stories</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {testimonials.map((t) => (
              <figure key={t.id} className="rounded-lg border border-gray-700 bg-gray-900 p-5">
                <blockquote className="text-sm leading-relaxed">&ldquo;{t.quote}&rdquo;</blockquote>
                <figcaption className="mt-3 text-sm">
                  <span className="font-medium">{t.name}</span>
                  <span className="text-gray-400"> • {t.role}</span>
                </figcaption>
              </figure>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section id="cta" className="w-full border-t border-gray-700 bg-gray-900">
          <div className="w-full px-4 md:px-6 py-12 text-center">
            <h2 className="text-xl md:text-2xl font-semibold">Ready to bring an idea to life?</h2>
            <p className="mt-2 text-sm text-gray-400">
              Join thousands of backers and creators moving ideas forward together.
            </p>
            <div className="mt-6 flex flex-col sm:flex-row items-center justify-center gap-3">
              <a
                href="#"
                className="inline-flex h-10 items-center justify-center rounded-md bg-indigo-600 px-5 text-sm font-medium text-white hover:bg-indigo-500"
              >
                Sign Up
              </a>
              <a
                href="#"
                className="inline-flex h-10 items-center justify-center rounded-md border border-gray-700 bg-gray-800 px-5 text-sm font-medium hover:bg-gray-700"
              >
                Start a Campaign
              </a>
              <a
                href="#"
                className="inline-flex h-10 items-center justify-center rounded-md border border-gray-700 bg-gray-800 px-5 text-sm font-medium hover:bg-gray-700"
              >
                Contact Us
              </a>
            </div>
          </div>
        </section>
      </main>
    </>
  )
}
