import { useQuery } from '@tanstack/react-query'
import { getHealth, getDocumentStats } from '../api/client'
import { Activity, Database, FileText, MessageSquare } from 'lucide-react'

export default function Dashboard() {
  const { data: health, isLoading: healthLoading } = useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
    refetchInterval: 30000
  })

  const { data: docs } = useQuery({
    queryKey: ['documents'],
    queryFn: getDocumentStats
  })

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">System Dashboard</h1>

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatusCard
          title="System Status"
          value={health?.data?.status || 'checking...'}
          icon={<Activity />}
          color={health?.data?.status === 'healthy' ? 'green' : 'yellow'}
        />
        <StatusCard
          title="Documents Indexed"
          value={docs?.data?.document_count || 0}
          icon={<FileText />}
          color="blue"
        />
        <StatusCard
          title="ChromaDB"
          value={health?.data?.checks?.chromadb?.includes('connected') ? 'Connected' : 'Checking...'}
          icon={<Database />}
          color="purple"
        />
        <StatusCard
          title="Ollama LLM"
          value={health?.data?.checks?.ollama?.includes('connected') ? 'Connected' : 'Checking...'}
          icon={<MessageSquare />}
          color="indigo"
        />
      </div>

      {/* Service Checks */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-lg font-semibold mb-4">Service Health Checks</h2>
        <div className="space-y-3">
          {health?.data?.checks && Object.entries(health.data.checks).map(([service, status]) => (
            <div key={service} className="flex justify-between items-center">
              <span className="font-medium capitalize">{service}</span>
              <span className={`px-3 py-1 rounded-full text-sm ${
                status.includes('connected') || status.includes('error') === false
                  ? 'bg-green-100 text-green-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {status}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <QuickAction label="Search Clients" href="/clients" />
          <QuickAction label="Ask Knowledge Base" href="/knowledge" />
          <QuickAction label="View Reports" href="/reports" />
          <QuickAction label="System Logs" href="#" />
        </div>
      </div>
    </div>
  )
}

function StatusCard({ title, value, icon, color }) {
  const colorClasses = {
    green: 'bg-green-50 text-green-600',
    blue: 'bg-blue-50 text-blue-600',
    purple: 'bg-purple-50 text-purple-600',
    indigo: 'bg-indigo-50 text-indigo-600',
    yellow: 'bg-yellow-50 text-yellow-600'
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <p className="text-2xl font-bold text-gray-800">{value}</p>
        </div>
        <div className={`p-3 rounded-full ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

function QuickAction({ label, href }) {
  return (
    <a
      href={href}
      className="block p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-center font-medium text-gray-700"
    >
      {label}
    </a>
  )
}
