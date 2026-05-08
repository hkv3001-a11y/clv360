export default function WeatherBar({ weather }) {
  if (!weather) {
    return (
      <div className="h-14 bg-slate-950 border-b border-slate-800 flex items-center px-6 text-slate-500 text-sm">
        Loading weather...
      </div>
    )
  }

  if (weather.error) {
    return (
      <div className="h-14 bg-slate-950 border-b border-slate-800 flex items-center px-6 text-red-400 text-sm">
        Weather unavailable
      </div>
    )
  }

  const isStormDay = (day) => ['⛈️', '🌧️'].includes(day.emoji)

  return (
    <div className="bg-slate-950 border-b border-slate-800 px-4 py-2 flex items-center gap-6 overflow-x-auto shrink-0">
      <div className="flex items-center gap-3 shrink-0">
        <span className="text-2xl">{weather.emoji}</span>
        <div>
          <div className="text-xl font-bold text-sky-400 leading-none">{weather.temp_f}°F</div>
          <div className="text-xs text-slate-400">{weather.location}</div>
        </div>
        <div className="text-xs text-slate-500 ml-1">
          <div>{weather.description}</div>
          <div>Wind {weather.wind_mph}mph · Humidity {weather.humidity}%</div>
        </div>
      </div>

      <div className="w-px h-8 bg-slate-800 shrink-0" />

      <div className="flex gap-3 items-center">
        {weather.forecast?.map((day, i) => (
          <div key={i} className={`flex flex-col items-center text-xs shrink-0 px-1.5 py-1 rounded-lg
            ${isStormDay(day) ? 'bg-amber-500/10 border border-amber-500/30' : ''}`}>
            <span className="text-slate-500">{day.day}</span>
            <span className="my-0.5">{day.emoji}</span>
            <span className={`font-medium ${isStormDay(day) ? 'text-amber-400' : 'text-slate-300'}`}>
              {day.high}°
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
