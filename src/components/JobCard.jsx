const STATUS_COLORS = {
  active: 'border-green-500',
  on_hold: 'border-amber-500',
  completed: 'border-slate-500',
  cancelled: 'border-red-500',
}
const STATUS_BADGES = {
  active: 'bg-green-500/20 text-green-400',
  on_hold: 'bg-amber-500/20 text-amber-400',
  completed: 'bg-slate-500/20 text-slate-400',
  cancelled: 'bg-red-500/20 text-red-400',
}

export default function JobCard({ job, crew, selected, onSelect, onEdit, onDelete }) {
  const crewMember = crew.find(c => c.id === job.crew_member_id)

  return (
    <div
      onClick={() => onSelect(job.id)}
      className={`bg-slate-800 rounded-lg p-3 border-l-4 cursor-pointer hover:bg-slate-750 transition-colors
        ${STATUS_COLORS[job.status] || 'border-slate-600'}
        ${selected ? 'ring-1 ring-indigo-500' : ''}`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="font-medium text-slate-100 truncate">{job.name}</div>
          {job.address && <div className="text-xs text-slate-400 truncate mt-0.5">{job.address}</div>}
        </div>
        <div className="flex gap-1 shrink-0">
          <button
            onClick={e => { e.stopPropagation(); onEdit(job) }}
            className="text-slate-400 hover:text-slate-200 text-xs px-1.5 py-0.5 rounded hover:bg-slate-700"
          >✎</button>
          <button
            onClick={e => { e.stopPropagation(); onDelete(job.id) }}
            className="text-slate-400 hover:text-red-400 text-xs px-1.5 py-0.5 rounded hover:bg-slate-700"
          >✕</button>
        </div>
      </div>
      <div className="flex items-center gap-2 mt-2">
        <span className={`text-xs px-1.5 py-0.5 rounded-full ${STATUS_BADGES[job.status] || ''}`}>
          {job.status.replace('_', ' ')}
        </span>
        {crewMember && <span className="text-xs text-slate-400">{crewMember.name}</span>}
        <span className="text-xs text-slate-500 ml-auto">{job.percent_complete}%</span>
      </div>
      <div className="mt-1.5 bg-slate-700 rounded-full h-1">
        <div
          className="bg-indigo-500 h-1 rounded-full transition-all"
          style={{ width: `${job.percent_complete}%` }}
        />
      </div>
    </div>
  )
}
