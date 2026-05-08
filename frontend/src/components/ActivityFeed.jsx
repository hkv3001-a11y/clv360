import { useState, useEffect } from 'react'
import { api } from '../api'

const CHANNEL_ICONS = {
  sms: '📱', whatsapp: '💬', email: '📧', manual: '✏️', ai: '🤖',
}

export default function ActivityFeed({ jobId }) {
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.jobs.activity(jobId).then(data => {
      setEntries(data || [])
      setLoading(false)
    })
  }, [jobId])

  if (loading) {
    return <div className="ml-4 mt-1 mb-2 p-3 text-xs text-slate-500 animate-pulse">Loading activity...</div>
  }

  return (
    <div className="ml-4 mt-1 mb-2 border-l-2 border-slate-700 pl-3 space-y-2">
      {entries.length === 0 && (
        <div className="text-xs text-slate-500 py-1">No activity yet.</div>
      )}
      {entries.map(entry => (
        <div key={entry.id} className="text-xs">
          <div className="flex items-center gap-1.5 text-slate-400">
            <span>{CHANNEL_ICONS[entry.channel] || '📋'}</span>
            <span className="font-medium text-slate-300">{entry.source_name || 'System'}</span>
            <span className="text-slate-600">·</span>
            <span className="text-slate-600">
              {new Date(entry.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
            </span>
          </div>
          {entry.raw_message && (
            <div className="text-slate-500 mt-0.5 ml-5 italic">"{entry.raw_message}"</div>
          )}
          {entry.parsed_action && (
            <div className="text-slate-400 mt-0.5 ml-5">{entry.parsed_action}</div>
          )}
        </div>
      ))}
    </div>
  )
}
