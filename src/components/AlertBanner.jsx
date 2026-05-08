export default function AlertBanner({ alerts, onDismiss }) {
  if (!alerts || alerts.length === 0) return null
  return (
    <div className="space-y-1 p-3 border-b border-slate-800">
      {alerts.map((alert, i) => (
        <div key={i} className="flex items-start gap-2 bg-amber-500/10 border border-amber-500/30 rounded-lg px-3 py-2 text-xs">
          <span>⚠️</span>
          <span className="text-amber-300 flex-1">{alert.message}</span>
          <button onClick={() => onDismiss(i)} className="text-slate-500 hover:text-slate-300">✕</button>
        </div>
      ))}
    </div>
  )
}
