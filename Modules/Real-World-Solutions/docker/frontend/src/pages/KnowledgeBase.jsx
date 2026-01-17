import { useState, useRef, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import { askQuestion, searchDocuments } from '../api/client'
import { MessageSquare, Send, FileText, User, Bot } from 'lucide-react'

export default function KnowledgeBase() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const messagesEndRef = useRef(null)

  const askMutation = useMutation({
    mutationFn: (q) => askQuestion(q),
    onSuccess: (data) => {
      setMessages(prev => [...prev, {
        type: 'assistant',
        content: data.data.answer,
        sources: data.data.sources
      }])
    },
    onError: (error) => {
      setMessages(prev => [...prev, {
        type: 'error',
        content: `Error: ${error.message}`
      }])
    }
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!question.trim()) return

    setMessages(prev => [...prev, { type: 'user', content: question }])
    askMutation.mutate(question)
    setQuestion('')
  }

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)]">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">Knowledge Base</h1>
      <p className="text-gray-500 mb-6">
        Ask questions about company policies, procedures, or merger documentation.
        Answers are generated using RAG from indexed documents.
      </p>

      {/* Chat Messages */}
      <div className="flex-1 bg-white rounded-lg shadow overflow-y-auto mb-4 p-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-400">
            <MessageSquare className="w-16 h-16 mb-4" />
            <p className="text-lg">Ask a question to get started</p>
            <div className="mt-6 space-y-2 text-sm">
              <SuggestedQuestion
                text="What are the payment terms for clients?"
                onClick={() => setQuestion("What are the payment terms for clients?")}
              />
              <SuggestedQuestion
                text="What did the CFO say about Q3 projections?"
                onClick={() => setQuestion("What did the CFO say about Q3 projections?")}
              />
              <SuggestedQuestion
                text="What are the audit procedures?"
                onClick={() => setQuestion("What are the audit procedures?")}
              />
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((msg, idx) => (
              <Message key={idx} message={msg} />
            ))}
            {askMutation.isPending && (
              <div className="flex items-center gap-2 text-gray-500">
                <Bot className="w-5 h-5 animate-pulse" />
                <span>Thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex gap-4">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about company knowledge..."
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={askMutation.isPending}
        />
        <button
          type="submit"
          disabled={askMutation.isPending || !question.trim()}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors flex items-center gap-2"
        >
          <Send className="w-4 h-4" />
          Send
        </button>
      </form>
    </div>
  )
}

function Message({ message }) {
  const isUser = message.type === 'user'
  const isError = message.type === 'error'

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : ''}`}>
      {!isUser && (
        <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
          isError ? 'bg-red-100' : 'bg-blue-100'
        }`}>
          <Bot className={`w-5 h-5 ${isError ? 'text-red-600' : 'text-blue-600'}`} />
        </div>
      )}
      <div className={`max-w-[70%] rounded-lg p-4 ${
        isUser
          ? 'bg-blue-600 text-white'
          : isError
          ? 'bg-red-50 text-red-800'
          : 'bg-gray-100 text-gray-800'
      }`}>
        <p className="whitespace-pre-wrap">{message.content}</p>
        {message.sources && message.sources.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs text-gray-500 mb-2">Sources:</p>
            <div className="space-y-1">
              {message.sources.map((source, idx) => (
                <div key={idx} className="flex items-center gap-1 text-xs text-gray-500">
                  <FileText className="w-3 h-3" />
                  {source.filename || source.source || 'Document'}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      {isUser && (
        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
          <User className="w-5 h-5 text-gray-600" />
        </div>
      )}
    </div>
  )
}

function SuggestedQuestion({ text, onClick }) {
  return (
    <button
      onClick={onClick}
      className="block w-full text-left px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
    >
      {text}
    </button>
  )
}
