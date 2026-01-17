import { useState } from 'react'
import { FileText, Download, Calendar, TrendingUp, Users, DollarSign } from 'lucide-react'

export default function Reports() {
  const [selectedReport, setSelectedReport] = useState(null)

  const reports = [
    {
      id: 'revenue_summary',
      name: 'Revenue Summary',
      description: 'Total revenue, collections, and outstanding balances',
      icon: <TrendingUp className="w-6 h-6" />,
      category: 'Financial'
    },
    {
      id: 'outstanding_ar',
      name: 'Outstanding A/R',
      description: 'All unpaid invoices with aging details',
      icon: <DollarSign className="w-6 h-6" />,
      category: 'Financial'
    },
    {
      id: 'client_aging',
      name: 'Client Aging Report',
      description: 'Aged receivables by client with buckets',
      icon: <Users className="w-6 h-6" />,
      category: 'Financial'
    },
    {
      id: 'data_quality',
      name: 'Data Quality Report',
      description: 'Issues found during ETL and their resolutions',
      icon: <FileText className="w-6 h-6" />,
      category: 'Integration'
    },
    {
      id: 'merge_status',
      name: 'Merge Status Report',
      description: 'Status of data integration from all sources',
      icon: <FileText className="w-6 h-6" />,
      category: 'Integration'
    }
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Reports</h1>

      {/* Report Categories */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <ReportCategory title="Financial Reports" count={3} color="blue" />
        <ReportCategory title="Integration Reports" count={2} color="purple" />
      </div>

      {/* Report List */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold">Available Reports</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {reports.map((report) => (
            <div
              key={report.id}
              className="p-4 hover:bg-gray-50 transition-colors cursor-pointer"
              onClick={() => setSelectedReport(report)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="p-2 bg-gray-100 rounded-lg text-gray-600">
                    {report.icon}
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">{report.name}</h3>
                    <p className="text-sm text-gray-500">{report.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs px-2 py-1 bg-gray-100 rounded-full text-gray-600">
                    {report.category}
                  </span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      alert(`Generating ${report.name}...`)
                    }}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                  >
                    <Download className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Report Preview Modal */}
      {selectedReport && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-auto">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-xl font-bold">{selectedReport.name}</h2>
              <p className="text-gray-500 mt-1">{selectedReport.description}</p>
            </div>
            <div className="p-6">
              <div className="bg-gray-50 rounded-lg p-8 text-center text-gray-500">
                <FileText className="w-12 h-12 mx-auto mb-4" />
                <p>Report preview will appear here</p>
                <p className="text-sm mt-2">
                  Connect to the MCP Financial Server to generate live reports
                </p>
              </div>
            </div>
            <div className="p-6 border-t border-gray-200 flex justify-end gap-3">
              <button
                onClick={() => setSelectedReport(null)}
                className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Close
              </button>
              <button
                onClick={() => {
                  alert(`Downloading ${selectedReport.name}...`)
                  setSelectedReport(null)
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                Download PDF
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function ReportCategory({ title, count, color }) {
  const colorClasses = {
    blue: 'bg-blue-50 border-blue-200 text-blue-600',
    purple: 'bg-purple-50 border-purple-200 text-purple-600'
  }

  return (
    <div className={`p-4 rounded-lg border-2 ${colorClasses[color]}`}>
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-medium">{title}</h3>
          <p className="text-2xl font-bold mt-1">{count}</p>
        </div>
        <Calendar className="w-8 h-8" />
      </div>
    </div>
  )
}
