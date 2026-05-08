import { useState } from 'react'
import { api } from '../api'
import JobCard from './JobCard'
import JobModal from './JobModal'
import ActivityFeed from './ActivityFeed'
import CrewModal from './CrewModal'

export default function JobsPanel({ jobs, crew, onJobsChange, onCrewChange }) {
  const [selectedJobId, setSelectedJobId] = useState(null)
  const [editingJob, setEditingJob] = useState(null)
  const [showNewJob, setShowNewJob] = useState(false)
  const [showCrew, setShowCrew] = useState(false)

  const handleCreate = async (data) => {
    await api.jobs.create(data)
    setShowNewJob(false)
    onJobsChange()
  }

  const handleEdit = async (data) => {
    await api.jobs.update(editingJob.id, data)
    setEditingJob(null)
    onJobsChange()
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this job?')) return
    await api.jobs.remove(id)
    if (selectedJobId === id) setSelectedJobId(null)
    onJobsChange()
  }

  return (
    <div className="w-3/5 flex flex-col border-r border-slate-800 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800">
        <h2 className="font-semibold text-slate-100">
          📋 Jobs <span className="text-slate-500 font-normal text-sm ml-1">({jobs.length})</span>
        </h2>
        <div className="flex gap-2">
          <button onClick={() => setShowCrew(true)}
            className="text-xs bg-slate-700 hover:bg-slate-600 px-3 py-1.5 rounded-lg text-slate-300">
            👥 Crew
          </button>
          <button onClick={() => setShowNewJob(true)}
            className="text-xs bg-indigo-600 hover:bg-indigo-500 px-3 py-1.5 rounded-lg font-medium">
            + Add Job
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {jobs.length === 0 && (
          <div className="text-center text-slate-500 py-12 text-sm">
            No jobs yet. Click "+ Add Job" to get started.
          </div>
        )}
        {jobs.map(job => (
          <div key={job.id}>
            <JobCard
              job={job}
              crew={crew}
              selected={selectedJobId === job.id}
              onSelect={(id) => setSelectedJobId(selectedJobId === id ? null : id)}
              onEdit={setEditingJob}
              onDelete={handleDelete}
            />
            {selectedJobId === job.id && (
              <ActivityFeed jobId={job.id} />
            )}
          </div>
        ))}
      </div>

      {showNewJob && (
        <JobModal crew={crew} onSave={handleCreate} onClose={() => setShowNewJob(false)} />
      )}
      {editingJob && (
        <JobModal job={editingJob} crew={crew} onSave={handleEdit} onClose={() => setEditingJob(null)} />
      )}
      {showCrew && (
        <CrewModal crew={crew} onCrewChange={onCrewChange} onClose={() => setShowCrew(false)} />
      )}
    </div>
  )
}
