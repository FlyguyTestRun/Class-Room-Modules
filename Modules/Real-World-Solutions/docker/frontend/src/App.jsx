import { useState } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { Building2, Search, MessageSquare, FileText, BarChart3 } from 'lucide-react'

// Pages
import Dashboard from './pages/Dashboard'
import ClientSearch from './pages/ClientSearch'
import KnowledgeBase from './pages/KnowledgeBase'
import Reports from './pages/Reports'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-100">
        {/* Sidebar */}
        <aside className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-blue-900 text-white transition-all duration-300`}>
          <div className="p-4">
            <h1 className={`font-bold ${sidebarOpen ? 'text-xl' : 'text-sm text-center'}`}>
              {sidebarOpen ? 'ZZZ Accounting' : 'ZZZ'}
            </h1>
            <p className={`text-blue-300 text-sm ${sidebarOpen ? '' : 'hidden'}`}>
              Merger Integration Platform
            </p>
          </div>

          <nav className="mt-8">
            <NavItem to="/" icon={<BarChart3 />} label="Dashboard" open={sidebarOpen} />
            <NavItem to="/clients" icon={<Building2 />} label="Client Search" open={sidebarOpen} />
            <NavItem to="/knowledge" icon={<MessageSquare />} label="Knowledge Base" open={sidebarOpen} />
            <NavItem to="/reports" icon={<FileText />} label="Reports" open={sidebarOpen} />
          </nav>

          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="absolute bottom-4 left-4 text-blue-300 hover:text-white"
          >
            {sidebarOpen ? '← Collapse' : '→'}
          </button>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-auto">
          <header className="bg-white shadow-sm p-4">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-gray-800">
                ZZZ + AAA + BBB Integration
              </h2>
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-500">
                  Connected to: <span className="text-green-600">3 databases</span>
                </span>
              </div>
            </div>
          </header>

          <div className="p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/clients" element={<ClientSearch />} />
              <Route path="/knowledge" element={<KnowledgeBase />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </div>
        </main>
      </div>
    </BrowserRouter>
  )
}

function NavItem({ to, icon, label, open }) {
  return (
    <Link
      to={to}
      className="flex items-center gap-3 px-4 py-3 hover:bg-blue-800 transition-colors"
    >
      <span className="w-6 h-6">{icon}</span>
      {open && <span>{label}</span>}
    </Link>
  )
}

export default App
