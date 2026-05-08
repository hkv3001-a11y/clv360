import { useState } from 'react'
import { api } from '../api'

export default function CrewModal({ crew, onCrewChange, onClose }) {
  const [newName, setNewName] = useState('')
  const [newPhone, setNewPhone] = useState('')
  const [editId, setEditId] = useState(null)
  const [editForm, setEditForm] = useState({})

  const handleAdd = async () => {
    if (!newName.trim()) return
    await api.crew.create({ name: newName.trim(), phone: newPhone.trim() })
    setNewName(''); setNewPhone('')
    onCrewChange()
  }

  const startEdit = (member) => {
    setEditId(member.id)
    setEditForm({ name: member.name, phone: member.phone, email: member.email })
  }

  const handleEditSave = async () => {
    await api.crew.update(editId, editForm)
    setEditId(null)
    onCrewChange()
  }

  const handleDelete = async (id) => {
    if (!confirm('Remove this crew member?')) return
    await api.crew.remove(id)
    onCrewChange()
  }

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-xl w-full max-w-lg border border-slate-700">
        <div className="flex items-center justify-between p-4 border-b border-slate-700">
          <h2 className="font-semibold">👥 Crew Members</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-white">✕</button>
        </div>

        <div className="p-4 border-b border-slate-700">
          <div className="flex gap-2">
            <input value={newName} onChange={e => setNewName(e.target.value)} placeholder="Name *"
              className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
            <input value={newPhone} onChange={e => setNewPhone(e.target.value)} placeholder="Phone"
              className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500" />
            <button onClick={handleAdd}
              className="bg-indigo-600 hover:bg-indigo-500 px-4 rounded-lg text-sm font-medium">Add</button>
          </div>
        </div>

        <div className="p-4 space-y-2 max-h-80 overflow-y-auto">
          {crew.length === 0 && <div className="text-sm text-slate-500 text-center py-4">No crew members yet.</div>}
          {crew.map(member => (
            <div key={member.id} className="bg-slate-900 rounded-lg p-3">
              {editId === member.id ? (
                <div className="flex gap-2">
                  <input value={editForm.name} onChange={e => setEditForm(f => ({...f, name: e.target.value}))}
                    className="flex-1 bg-slate-800 border border-slate-600 rounded px-2 py-1 text-sm focus:outline-none" />
                  <input value={editForm.phone} onChange={e => setEditForm(f => ({...f, phone: e.target.value}))}
                    className="flex-1 bg-slate-800 border border-slate-600 rounded px-2 py-1 text-sm focus:outline-none" />
                  <button onClick={handleEditSave} className="text-green-400 text-sm px-2">✓</button>
                  <button onClick={() => setEditId(null)} className="text-slate-400 text-sm px-2">✕</button>
                </div>
              ) : (
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-slate-200">{member.name}</div>
                    {member.phone && <div className="text-xs text-slate-500">{member.phone}</div>}
                  </div>
                  <div className="flex gap-1">
                    <button onClick={() => startEdit(member)} className="text-slate-400 hover:text-slate-200 text-xs px-2 py-1 rounded hover:bg-slate-700">✎</button>
                    <button onClick={() => handleDelete(member.id)} className="text-slate-400 hover:text-red-400 text-xs px-2 py-1 rounded hover:bg-slate-700">✕</button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
