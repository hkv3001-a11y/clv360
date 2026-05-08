import { useState, useEffect } from 'react'

export default function JobModal({ job, crew, onSave, onClose }) {
  const [form, setForm] = useState({
    name: '', address: '', status: 'active',
    crew_member_id: '', percent_complete: 0,
    start_date: '', target_date: '',
  })

  useEffect(() => {
    if (job) setForm({
      name: job.name || '',
      address: job.address || '',
      status: job.status || 'active',
      crew_member_id: job.crew_member_id ?? '',
      percent_complete: job.percent_complete ?? 0,
      start_date: job.start_date || '',
      target_date: job.target_date || '',
    })
  }, [job])

  const set = (field) => (e) => setForm(f => ({ ...f, [field]: e.target.value }))

  const handleSubmit = (e) => {
    e.preventDefault()
    onSave({
      ...form,
      crew_member_id: form.crew_member_id ? parseInt(form.crew_member_id) : null,
      percent_complete: parseInt(form.percent_complete),
    })
  }

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-xl w-full max-w-md border border-slate-700">
        <div className="flex items-center justify-between p-4 border-b border-slate-700">
          <h2 className="font-semibold">{job ? 'Edit Job' : 'New Job'}</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-white">✕</button>
        </div>
        <form onSubmit={handleSubmit} className="p-4 space-y-3">
          <input required value={form.name} onChange={set('name')} placeholder="Job name *"
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
          <input value={form.address} onChange={set('address')} placeholder="Address"
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
          <div className="flex gap-2">
            <select value={form.status} onChange={set('status')}
              className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500">
              <option value="active">Active</option>
              <option value="on_hold">On Hold</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
            <select value={form.crew_member_id} onChange={set('crew_member_id')}
              className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500">
              <option value="">No crew assigned</option>
              {crew.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </div>
          <div>
            <label className="text-xs text-slate-400 mb-1 block">Completion: {form.percent_complete}%</label>
            <input type="range" min="0" max="100" value={form.percent_complete} onChange={set('percent_complete')}
              className="w-full accent-indigo-500" />
          </div>
          <div className="flex gap-2">
            <input type="date" value={form.start_date} onChange={set('start_date')}
              className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
            <input type="date" value={form.target_date} onChange={set('target_date')}
              className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
          </div>
          <div className="flex gap-2 pt-2">
            <button type="button" onClick={onClose}
              className="flex-1 bg-slate-700 hover:bg-slate-600 rounded-lg py-2 text-sm">Cancel</button>
            <button type="submit"
              className="flex-1 bg-indigo-600 hover:bg-indigo-500 rounded-lg py-2 text-sm font-medium">
              {job ? 'Save Changes' : 'Create Job'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
