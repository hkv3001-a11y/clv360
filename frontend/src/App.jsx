import { useState, useEffect } from 'react'
import { api } from './api'
import WeatherBar from './components/WeatherBar'
import JobsPanel from './components/JobsPanel'
import ChatPanel from './components/ChatPanel'

export default function App() {
  const [jobs, setJobs] = useState([])
  const [crew, setCrew] = useState([])
  const [weather, setWeather] = useState(null)
  const [alerts, setAlerts] = useState([])

  const refreshJobs = async () => setJobs(await api.jobs.list())
  const refreshCrew = async () => setCrew(await api.crew.list())

  useEffect(() => {
    refreshJobs()
    refreshCrew()
    api.weather.get().then(setWeather)
    api.alerts.get().then(d => setAlerts(d?.alerts || []))
  }, [])

  return (
    <div className="flex flex-col h-screen bg-slate-900 text-slate-100">
      <WeatherBar weather={weather} />
      <div className="flex flex-1 overflow-hidden">
        <JobsPanel
          jobs={jobs}
          crew={crew}
          onJobsChange={refreshJobs}
          onCrewChange={refreshCrew}
        />
        <ChatPanel
          alerts={alerts}
          onJobsChange={refreshJobs}
        />
      </div>
    </div>
  )
}
