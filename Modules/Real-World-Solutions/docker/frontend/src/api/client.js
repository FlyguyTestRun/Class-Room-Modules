import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Health check
export const getHealth = () => api.get('/health')

// Document search
export const searchDocuments = (query, limit = 5) =>
  api.post('/api/v1/search', { query, limit })

// Ask question (RAG)
export const askQuestion = (question) =>
  api.post('/api/v1/ask', { question })

// Chat (no RAG)
export const chat = (message) =>
  api.post('/api/v1/chat', { message })

// Client search
export const searchClients = (query) =>
  api.get(`/api/v1/clients/search?q=${encodeURIComponent(query)}`)

// Get document stats
export const getDocumentStats = () =>
  api.get('/api/v1/documents')

// List models
export const getModels = () =>
  api.get('/api/v1/models')
