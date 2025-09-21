import React from 'react'
import { motion } from 'framer-motion'

// AdvancedUI.jsx
// Single-file React component showcasing an advanced, innovative, and attractive UI/UX
// Built for Tailwind CSS utility-first styling and Framer Motion for smooth interactions.
// NOTE: This is intentionally self-contained as a single-file exportable React component.

// ---------- Helper data ----------
const features = [
  {
    id: 1,
    title: 'Dynamic Gradients',
    desc: 'Animated multi-layered gradients that respond to pointer position.',
    icon: '🌈'
  },
  {
    id: 2,
    title: 'Glassmorphism Cards',
    desc: 'Frosted glass panels with soft shadows and blur.',
    icon: '💠'
  },
  {
    id: 3,
    title: 'Neumorphic Controls',
    desc: 'Tactile buttons and toggles with depth and micro-interactions.',
    icon: '🔘'
  },
  {
    id: 4,
    title: 'Micro-interactions',
    desc: 'Subtle motion that gives the UI a polished feel.',
    icon: '🪄'
  }
]

const sampleStats = [
  { id: 's1', label: 'Active Users', value: '28.4K' },
  { id: 's2', label: 'Conversion', value: '6.2%' },
  { id: 's3', label: 'Avg. Session', value: '4m 21s' },
  { id: 's4', label: 'Bounce', value: '18%' }
]

// ---------- SVG Decorations ----------
function AuraSVG({ className = '' }) {
  return (
    <svg className={className} viewBox="0 0 800 600" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden>
      <defs>
        <linearGradient id="lg1" x1="0%" x2="100%">
          <stop offset="0%" stopColor="#7C3AED" stopOpacity="0.9" />
          <stop offset="50%" stopColor="#06B6D4" stopOpacity="0.8" />
          <stop offset="100%" stopColor="#F97316" stopOpacity="0.7" />
        </linearGradient>
        <filter id="f1" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="50" />
        </filter>
      </defs>

      <g filter="url(#f1)">
        <ellipse cx="220" cy="160" rx="260" ry="120" fill="url(#lg1)" />
        <ellipse cx="560" cy="420" rx="220" ry="110" fill="#60A5FA" opacity="0.5" />
      </g>
    </svg>
  )
}

// ---------- Subcomponents ----------

function Tag({ children }) {
  return (
    <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-white/10 backdrop-blur-sm ring-1 ring-white/6">{children}</span>
  )
}

function StatCard({ label, value }) {
  return (
    <div className="p-4 rounded-2xl bg-white/6 backdrop-blur-md ring-1 ring-white/6 flex-1 min-w-[150px]">
      <div className="text-2xl font-semibold">{value}</div>
      <div className="text-xs text-white/70 mt-1">{label}</div>
    </div>
  )
}

function FeatureCard({ icon, title, desc, index }) {
  const delay = 0.1 * index
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay, duration: 0.5 }} className="p-5 rounded-2xl bg-gradient-to-br from-white/3 to-white/6 ring-1 ring-white/5 backdrop-blur-md">
      <div className="text-xl">{icon}</div>
      <h3 className="mt-3 font-semibold text-lg">{title}</h3>
      <p className="text-sm text-white/80 mt-2">{desc}</p>
    </motion.div>
  )
}

function AnimatedToggle({ checked, onChange }) {
  return (
    <button onClick={() => onChange(!checked)} aria-pressed={checked} className="relative inline-flex items-center h-8 w-14 rounded-full p-1 bg-white/6 ring-1 ring-white/6 transition-all">
      <motion.span layout className={`h-6 w-6 rounded-full bg-white shadow-sm`} style={{ boxShadow: '0 6px 18px rgba(0,0,0,0.25)' }} />
    </button>
  )
}

// ---------- Large Utility Panel (many UI elements combined) ----------
function ControlPanel() {
  const [enabled, setEnabled] = React.useState(true)
  const [query, setQuery] = React.useState('')
  return (
    <div className="p-6 rounded-3xl bg-gradient-to-br from-white/5 to-white/3 ring-1 ring-white/6 backdrop-blur-md w-full">
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="text-sm text-white/80">Realtime</div>
          <div className="text-2xl font-bold">Dashboard Controls</div>
        </div>
        <div className="flex items-center gap-3">
          <Tag>Beta</Tag>
          <AnimatedToggle checked={enabled} onChange={setEnabled} />
        </div>
      </div>

      <div className="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="flex items-center gap-3">
          <div className="flex-1">
            <label className="text-xs text-white/70">Search</label>
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search metrics, users, reports..." className="mt-2 w-full rounded-xl p-3 bg-white/5 ring-1 ring-white/6 outline-none" />
          </div>
          <button className="px-4 py-3 rounded-xl bg-white/8 ring-1 ring-white/6">Go</button>
        </div>

        <div className="flex gap-3 items-center">
          <div className="flex-1">
            <label className="text-xs text-white/70">Range</label>
            <select className="mt-2 w-full rounded-xl p-3 bg-white/5 ring-1 ring-white/6">
              <option>Last 7 days</option>
              <option>Last 30 days</option>
              <option>Last 90 days</option>
            </select>
          </div>
          <div className="w-20 text-center">
            <label className="text-xs text-white/70">Sync</label>
            <div className="mt-2">{enabled ? 'On' : 'Off'}</div>
          </div>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-3">
        {sampleStats.map(s => <StatCard key={s.id} label={s.label} value={s.value} />)}
      </div>

      <div className="mt-6 flex gap-3">
        <button className="px-5 py-3 rounded-2xl bg-gradient-to-r from-indigo-500/80 to-cyan-400/80 text-black font-semibold shadow-2xl">Primary Action</button>
        <button className="px-5 py-3 rounded-2xl bg-white/6 ring-1 ring-white/6">Secondary</button>
        <button className="px-5 py-3 rounded-2xl bg-transparent ring-1 ring-white/6">Ghost</button>
      </div>
    </div>
  )
}

// ---------- Complex Interactive Graph Mockup (SVG + interactions) ----------
function SparkGraph({ width = 600, height = 200 }) {
  // Generate sample path points
  const points = React.useMemo(() => {
    const arr = []
    for (let i = 0; i < 12; i++) {
      const x = (i / 11) * width
      const y = height / 2 + Math.sin(i * 0.9) * (height / 3) + (Math.random() - 0.5) * 20
      arr.push([x, y])
    }
    return arr
  }, [width, height])

  const d = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p[0].toFixed(2)} ${p[1].toFixed(2)}`).join(' ')
  return (
    <svg viewBox={`0 0 ${width} ${height}`} width="100%" className="rounded-2xl overflow-hidden">
      <defs>
        <linearGradient id="gLine" x1="0" x2="1">
          <stop offset="0%" stopColor="#7C3AED" stopOpacity="1" />
          <stop offset="100%" stopColor="#06B6D4" stopOpacity="1" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#bg)" />
      <path d={d} fill="none" stroke="url(#gLine)" strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />
      {points.map((p, i) => (
        <motion.circle key={i} cx={p[0]} cy={p[1]} r={4} whileHover={{ r: 7 }} transition={{ type: 'spring', stiffness: 300 }} />
      ))}
    </svg>
  )
}

// ---------- Complex Card Grid with layered effects ----------
function DashboardCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <motion.div initial={{ scale: 0.98 }} whileHover={{ scale: 1.02 }} className="p-6 rounded-3xl bg-gradient-to-br from-white/4 to-white/6 ring-1 ring-white/6 backdrop-blur-md">
        <div className="flex items-center justify-between">
          <h4 className="font-semibold">Overview</h4>
          <Tag>Live</Tag>
        </div>
        <div className="mt-4">
          <SparkGraph width={480} height={140} />
        </div>
      </motion.div>

      <motion.div initial={{ x: -10, opacity: 0.9 }} whileHover={{ x: 0 }} className="p-6 rounded-3xl bg-gradient-to-br from-white/4 to-white/6 ring-1 ring-white/6 backdrop-blur-md">
        <h4 className="font-semibold">Top Converting Pages</h4>
        <ul className="mt-4 space-y-3">
          <li className="flex items-center justify-between"><div className="flex items-center gap-3"><span className="w-8 h-8 rounded-md bg-white/6 grid place-items-center">1</span><div className="text-sm">Landing / Checkout</div></div><div className="text-sm font-semibold">4.6%</div></li>
          <li className="flex items-center justify-between"><div className="flex items-center gap-3"><span className="w-8 h-8 rounded-md bg-white/6 grid place-items-center">2</span><div className="text-sm">Pricing</div></div><div className="text-sm font-semibold">3.8%</div></li>
        </ul>
      </motion.div>

      <motion.div className="p-6 rounded-3xl bg-gradient-to-br from-white/4 to-white/6 ring-1 ring-white/6 backdrop-blur-md">
        <h4 className="font-semibold">User Cohorts</h4>
        <div className="mt-4 grid grid-cols-2 gap-3">
          <div className="p-3 rounded-lg bg-white/5">New: <div className="font-bold">6.1K</div></div>
          <div className="p-3 rounded-lg bg-white/5">Returning: <div className="font-bold">22.3K</div></div>
        </div>
        <div className="mt-4">Quick filters</div>
      </motion.div>
    </div>
  )
}

// ---------- Complex Hero with pointer-reactive gradient ----------
function Hero() {
  const ref = React.useRef(null)
  const [pos, setPos] = React.useState({ x: 50, y: 50 })

  React.useEffect(() => {
    const el = ref.current
    if (!el) return
    function onMove(e) {
      const rect = el.getBoundingClientRect()
      const x = ((e.clientX - rect.left) / rect.width) * 100
      const y = ((e.clientY - rect.top) / rect.height) * 100
      setPos({ x, y })
    }
    el.addEventListener('pointermove', onMove)
    return () => el.removeEventListener('pointermove', onMove)
  }, [])

  return (
    <section ref={ref} className="relative overflow-hidden rounded-3xl p-8" aria-label="hero">
      <div className="absolute inset-0 pointer-events-none">
        <div style={{ transform: `translate(${(pos.x - 50) * 0.6}px, ${(pos.y - 50) * 0.6}px)` }} className="absolute -left-20 -top-40 w-[600px] h-[600px] opacity-80">
          <AuraSVG />
        </div>
      </div>

      <div className="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
        <div>
          <Tag>Showcase</Tag>
          <h1 className="mt-4 text-4xl md:text-6xl font-extrabold leading-tight">Innovative UI — Designed to Delight</h1>
          <p className="mt-4 text-lg text-white/80 max-w-xl">A packed component demo of advanced UI patterns: dynamic gradients, glassmorphism, micro-interactions and dashboards, all composed into a modern and extensible design system.</p>

          <div className="mt-6 flex gap-3">
            <button className="px-6 py-3 rounded-2xl bg-gradient-to-r from-indigo-500 to-cyan-400 text-black font-semibold shadow-lg">Get the Code</button>
            <button className="px-6 py-3 rounded-2xl bg-white/6 ring-1 ring-white/6">Live Demo</button>
          </div>
        </div>

        <div>
          <div className="p-4 rounded-2xl bg-white/3 ring-1 ring-white/6 backdrop-blur-md">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs text-white/70">Conversion Rate</div>
                <div className="text-2xl font-semibold">4.6%</div>
              </div>
              <div className="text-sm text-white/70">This week</div>
            </div>

            <div className="mt-4">
              <SparkGraph width={360} height={120} />
            </div>

            <div className="mt-4 grid grid-cols-3 gap-2">
              <div className="p-2 rounded-lg text-center bg-white/5">CTR<div className="font-bold">3.2%</div></div>
              <div className="p-2 rounded-lg text-center bg-white/5">CVR<div className="font-bold">1.5%</div></div>
              <div className="p-2 rounded-lg text-center bg-white/5">ARPU<div className="font-bold">₹420</div></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

// ---------- Footer micro-UX component ----------
function ComplexFooter() {
  return (
    <footer className="mt-12 p-6 rounded-2xl bg-gradient-to-tr from-white/4 to-white/6 ring-1 ring-white/6 backdrop-blur-md">
      <div className="flex items-center justify-between">
        <div className="text-sm">© {new Date().getFullYear()} SUPREETH — Advanced UI Demo</div>
        <div className="flex items-center gap-3">
          <a className="text-sm text-white/80">Privacy</a>
          <a className="text-sm text-white/80">Terms</a>
        </div>
      </div>
    </footer>
  )
}

// ---------- Long list of small components to reach advanced complexity ----------
function Chip({ children }) {
  return <span className="px-2 py-1 rounded-full text-xs bg-white/6 ring-1 ring-white/5">{children}</span>
}

function FancyList({ items = [] }) {
  return (
    <ol className="space-y-3 list-decimal pl-5">
      {items.map((it, i) => (
        <li key={i} className="text-sm text-white/85">{it}</li>
      ))}
    </ol>
  )
}

function MultiColumnShowcase() {
  const list = new Array(8).fill(0).map((_, i) => `Creative pattern ${i + 1}`)
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="p-4 rounded-2xl bg-white/5 ring-1 ring-white/6">
        <h5 className="font-semibold">Patterns</h5>
        <FancyList items={list.slice(0, 4)} />
      </div>
      <div className="p-4 rounded-2xl bg-white/5 ring-1 ring-white/6">
        <h5 className="font-semibold">Components</h5>
        <FancyList items={list.slice(4)} />
      </div>
    </div>
  )
}

// ---------- Massive example panel: a pseudo settings page, long form controls ----------
function SettingsPanel() {
  return (
    <div className="p-6 rounded-3xl bg-gradient-to-r from-white/5 to-white/3 ring-1 ring-white/6">
      <h3 className="font-bold">Appearance & Behaviour</h3>
      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-3">
          <label className="text-sm text-white/80">Theme</label>
          <div className="flex gap-2">
            <button className="px-4 py-2 rounded-xl bg-white/6 ring-1 ring-white/6">Light</button>
            <button className="px-4 py-2 rounded-xl bg-white/6 ring-1 ring-white/6">Dark</button>
            <button className="px-4 py-2 rounded-xl bg-white/6 ring-1 ring-white/6">System</button>
          </div>

          <label className="mt-3 text-sm text-white/80">Accent</label>
          <div className="flex gap-2 items-center">
            <div className="w-8 h-8 rounded-full bg-indigo-500" />
            <div className="w-8 h-8 rounded-full bg-cyan-400" />
            <div className="w-8 h-8 rounded-full bg-rose-400" />
          </div>
        </div>

        <div className="space-y-3">
          <label className="text-sm text-white/80">Layout density</label>
          <div className="flex gap-2">
            <button className="px-3 py-2 rounded-lg bg-white/6">Comfortable</button>
            <button className="px-3 py-2 rounded-lg bg-white/6">Compact</button>
          </div>

          <label className="mt-3 text-sm text-white/80">Motion</label>
          <div className="flex gap-2 items-center">
            <Chip>Reduced</Chip>
            <Chip>Normal</Chip>
            <Chip>Dynamic</Chip>
          </div>
        </div>
      </div>

      <div className="mt-6">
        <h4 className="font-semibold">Advanced</h4>
        <p className="text-sm text-white/80">Toggle dev options for experimental component rendering and debug overlays.</p>
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="p-3 rounded-lg bg-white/5">Rendering: <div className="font-bold">WebGL</div></div>
          <div className="p-3 rounded-lg bg-white/5">Shadows: <div className="font-bold">Soft</div></div>
          <div className="p-3 rounded-lg bg-white/5">Perf mode: <div className="font-bold">Balanced</div></div>
        </div>
      </div>
    </div>
  )
}

// ---------- Large illustrative grid to increase lines and show a design system ----------
function ComponentShowcase() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div className="p-4 rounded-2xl bg-white/5 ring-1 ring-white/6">
        <h5 className="font-semibold">Buttons</h5>
        <div className="mt-3 flex flex-wrap gap-2">
          <button className="px-3 py-2 rounded-md">Default</button>
          <button className="px-3 py-2 rounded-md bg-indigo-500 text-black">Primary</button>
          <button className="px-3 py-2 rounded-md bg-white/6">Ghost</button>
        </div>
      </div>

      <div className="p-4 rounded-2xl bg-white/5 ring-1 ring-white/6">
        <h5 className="font-semibold">Inputs</h5>
        <div className="mt-3 space-y-2">
          <input placeholder="Text input" className="w-full p-2 rounded-lg bg-white/6" />
          <select className="w-full p-2 rounded-lg bg-white/6"><option>Option A</option></select>
        </div>
      </div>

      <div className="p-4 rounded-2xl bg-white/5 ring-1 ring-white/6">
        <h5 className="font-semibold">Lists</h5>
        <ul className="mt-3 space-y-2">
          <li className="p-2 rounded-lg bg-white/6">List item one</li>
          <li className="p-2 rounded-lg bg-white/6">List item two</li>
        </ul>
      </div>

      <div className="p-4 rounded-2xl bg-white/5 ring-1 ring-white/6">
        <h5 className="font-semibold">Avatars</h5>
        <div className="mt-3 flex items-center gap-2">
          <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-400 to-cyan-300 grid place-items-center">A</div>
          <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-rose-300 to-yellow-300 grid place-items-center">B</div>
        </div>
      </div>

      <div className="p-4 rounded-2xl bg-white/5 ring-1 ring-white/6">
        <h5 className="font-semibold">Badges</h5>
        <div className="mt-3 flex gap-2">
          <Tag>New</Tag>
          <Tag>Updated</Tag>
          <Tag>Live</Tag>
        </div>
      </div>

      <div className="p-4 rounded-2xl bg-white/5 ring-1 ring-white/6">
        <h5 className="font-semibold">Tooltips (mock)</h5>
        <div className="mt-3 flex gap-2 items-center">
          <div className="group relative">
            <button className="px-3 py-2 rounded-md">Hover</button>
            <div className="absolute -top-10 left-0 hidden group-hover:block p-2 rounded-md bg-black text-white text-xs">Tooltip text</div>
          </div>
        </div>
      </div>
    </div>
  )
}

// ---------- Main Exported Component (big composition) ----------
export default function AdvancedUI() {
  return (
    <div className="min-h-screen p-8 bg-gradient-to-br from-slate-900 to-slate-800 text-white font-sans">
      <div className="max-w-[1400px] mx-auto">
        {/* Top nav */}
        <nav className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-tr from-indigo-500 to-cyan-400 grid place-items-center font-bold text-black">SI</div>
            <div>
              <div className="font-extrabold">SUPREETH UI</div>
              <div className="text-xs text-white/70">Design system preview</div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <input placeholder="Quick search..." className="rounded-xl p-2 bg-white/6 ring-1 ring-white/6" />
            <div className="flex items-center gap-2">
              <button className="px-3 py-2 rounded-lg">Docs</button>
              <button className="px-3 py-2 rounded-lg bg-white/6">Sign in</button>
            </div>
          </div>
        </nav>

        <main className="space-y-8">
          <Hero />

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <ControlPanel />

              <div className="mt-6">
                <h3 className="font-bold mb-4">Dashboard</h3>
                <DashboardCards />
              </div>

              <div className="mt-6">
                <h3 className="font-bold mb-4">Components</h3>
                <ComponentShowcase />
              </div>

              <div className="mt-6">
                <h3 className="font-bold mb-4">Settings</h3>
                <SettingsPanel />
              </div>
            </div>

            <aside className="space-y-6">
              <div className="p-4 rounded-2xl bg-white/4 ring-1 ring-white/6">
                <h4 className="font-semibold">Quick Actions</h4>
                <div className="mt-3 flex flex-col gap-3">
                  <button className="p-3 rounded-lg text-left bg-white/5">Create Report</button>
                  <button className="p-3 rounded-lg text-left bg-white/5">Export Data</button>
                  <button className="p-3 rounded-lg text-left bg-white/5">Invite Team</button>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-white/4 ring-1 ring-white/6">
                <h4 className="font-semibold">Features</h4>
                <div className="mt-3 space-y-3">
                  {features.map((f, i) => <FeatureCard key={f.id} index={i} {...f} />)}
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-white/4 ring-1 ring-white/6">
                <h4 className="font-semibold">Showcase</h4>
                <MultiColumnShowcase />
              </div>
            </aside>
          </div>

          <div>
            <h3 className="font-bold mb-4">Design Tokens & Notes</h3>
            <div className="p-4 rounded-2xl bg-white/6 ring-1 ring-white/6">
              <p className="text-sm text-white/80">Use Tailwind CSS as the utility engine. Add these global tokens to extend your theme: primary gradient, glass card background, subtle ring color and elevated shadows. Consider adding a CSS variable map for user-selectable accents.</p>

              <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="p-3 rounded-lg bg-white/5 text-center">--accent: #7C3AED</div>
                <div className="p-3 rounded-lg bg-white/5 text-center">--accent-2: #06B6D4</div>
                <div className="p-3 rounded-lg bg-white/5 text-center">--glass: rgba(255,255,255,0.06)</div>
                <div className="p-3 rounded-lg bg-white/5 text-center">--ring: rgba(255,255,255,0.06)</div>
              </div>
            </div>
          </div>

          <div>
            <h3 className="font-bold mb-4">Playground</h3>
            <div className="p-4 rounded-2xl bg-white/5 ring-1 ring-white/6">
              <p className="text-sm text-white/80">This playground section intentionally contains a lot of small interactive elements for you to copy-paste and adapt. Each microcomponent demonstrates a pattern you can reuse.</p>
              <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="p-3 rounded-lg bg-white/6">Switches<div className="mt-2"><AnimatedToggle checked={true} onChange={() => {}} /></div></div>
                <div className="p-3 rounded-lg bg-white/6">Progress<div className="mt-2 w-full bg-white/8 rounded-full h-3 overflow-hidden"><div style={{ width: '64%' }} className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-cyan-400" /></div></div>
                <div className="p-3 rounded-lg bg-white/6">Loader<div className="mt-2"><div className="animate-spin w-6 h-6 border-2 border-transparent border-t-white rounded-full" /></div></div>
              </div>
            </div>
          </div>

          <ComplexFooter />
        </main>
      </div>
    </div>
  )
}

// End of single-file component
