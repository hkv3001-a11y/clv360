import { useState, useRef, useEffect } from 'react'
import { api } from '../api'
import AlertBanner from './AlertBanner'

export default function ChatPanel({ alerts: initialAlerts, onJobsChange }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: "Hi! I'm your CLV360 assistant. Ask me about your jobs, crew, or tell me to update a job status." }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [alerts, setAlerts] = useState(initialAlerts || [])
  const bottomRef = useRef(null)

  useEffect(() => setAlerts(initialAlerts || []), [initialAlerts])
  useEffect(() => bottomRef.current?.scrollIntoView({ behavior: 'smooth' }), [messages])

  const send = async () => {
    const text = input.trim()
    if (!text || loading) return
    setInput('')
    setMessages(m => [...m, { role: 'user', text }])
    setLoading(true)
    try {
      const data = await api.chat.send(text)
      setMessages(m => [...m, { role: 'assistant', text: data.response }])
      if (data.action_taken) onJobsChange()
    } catch {
      setMessages(m => [...m, { role: 'assistant', text: 'Sorry, something went wrong. Check that the backend is running.' }])
    }
    setLoading(false)
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
  }

  return (
    <div className="w-2/5 flex flex-col bg-slate-900">
      <div className="px-4 py-3 border-b border-slate-800">
        <h2 className="font-semibold text-slate-100">🤖 AI Assistant</h2>
      </div>

      <AlertBanner alerts={alerts} onDismiss={(i) => setAlerts(a => a.filter((_, idx) => idx !== i))} />

      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] px-3 py-2 rounded-xl text-sm leading-relaxed
              ${m.role === 'user'
                ? 'bg-indigo-600 text-white rounded-br-sm'
                : 'bg-slate-800 text-slate-200 rounded-bl-sm'}`}>
              {m.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-800 px-3 py-2 rounded-xl rounded-bl-sm text-slate-400 text-sm">
              <span className="animate-pulse">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="p-3 border-t border-slate-800">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Ask me anything... (Enter to send)"
            rows={2}
            className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm resize-none focus:outline-none focus:border-indigo-500 text-slate-100 placeholder-slate-500"
          />
          <button
            onClick={send}
            disabled={loading || !input.trim()}
            className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 px-4 rounded-xl text-sm font-medium self-end py-2"
          >Send</button>
        </div>
      </div>
    </div>
  )
}
