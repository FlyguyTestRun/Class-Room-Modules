import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { searchClients } from '../api/client'
import { Search, Building2, Mail, Phone } from 'lucide-react'

export default function ClientSearch() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])

  const searchMutation = useMutation({
    mutationFn: (q) => searchClients(q),
    onSuccess: (data) => {
      setResults(data.data.results || [])
    }
  })

  const handleSearch = (e) => {
    e.preventDefault()
    if (query.trim()) {
      searchMutation.mutate(query)
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Client Search</h1>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-8">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search clients by name, tax ID, or contact..."
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            disabled={searchMutation.isPending}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {searchMutation.isPending ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {/* Results */}
      {results.length > 0 ? (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Client</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tax ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {results.map((client) => (
                <tr key={client.org_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <Building2 className="w-5 h-5 text-gray-400 mr-3" />
                      <div>
                        <div className="font-medium text-gray-900">{client.legal_name}</div>
                        {client.dba_name && (
                          <div className="text-sm text-gray-500">DBA: {client.dba_name}</div>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-gray-500">
                    {client.tax_id || 'N/A'}
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                      {client.org_type}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : searchMutation.isSuccess ? (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">No clients found matching "{query}"</p>
        </div>
      ) : (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <Building2 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">Search for clients across all merged databases</p>
          <p className="text-sm text-gray-400 mt-2">
            Data sources: ZZZ Accounting, AAA Accounting, BBB Construction
          </p>
        </div>
      )}
    </div>
  )
}
