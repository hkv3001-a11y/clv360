const BASE = ''  // proxied through Vite to http://localhost:8000 in dev; /api on Vercel

async function req(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (res.status === 204) return null
  return res.json()
}

export const api = {
  jobs: {
    list: () => req('/api/jobs'),
    create: (data) => req('/api/jobs', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => req(`/api/jobs/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    remove: (id) => req(`/api/jobs/${id}`, { method: 'DELETE' }),
    activity: (id) => req(`/api/jobs/${id}/activity`),
    addActivity: (id, data) => req(`/api/jobs/${id}/activity`, { method: 'POST', body: JSON.stringify(data) }),
  },
  crew: {
    list: () => req('/api/crew'),
    create: (data) => req('/api/crew', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => req(`/api/crew/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    remove: (id) => req(`/api/crew/${id}`, { method: 'DELETE' }),
  },
  chat: {
    send: (message) => req('/api/chat', { method: 'POST', body: JSON.stringify({ message }) }),
  },
  weather: {
    get: () => req('/api/weather'),
  },
  alerts: {
    get: () => req('/api/alerts'),
  },
  inbound: {
    test: (data) => req('/api/inbound/test', { method: 'POST', body: JSON.stringify(data) }),
  },
}
