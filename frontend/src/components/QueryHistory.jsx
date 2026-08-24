import React from 'react';

/**
 * SatQuery AI — Query History Component (Stitch Design)
 */
export default function QueryHistory({ history = [], onReplayQuery, onClearHistory }) {
  const sampleHistory = history.length > 0 ? history : [
    {
      id: 'QRY-8842-CD',
      query: 'Identify new structures built between the two dates and estimate their area.',
      mode: 'change',
      modeLabel: 'Change Detection',
      timestamp: '2026-08-24 14:05:12',
      confidence: 0.874,
      latencyMs: 385,
      answer: 'Significant urban expansion detected in the northwest quadrant (+12%). Several new industrial warehouses identified.',
    },
    {
      id: 'QRY-8841-FS',
      query: 'Where are the flood-affected regions and how much did water extent increase?',
      mode: 'fusion',
      modeLabel: 'Optical + SAR Fusion',
      timestamp: '2026-08-24 13:42:09',
      confidence: 0.912,
      latencyMs: 410,
      answer: 'Flood extent increased by 28.4% across coastal plain. SAR backscatter corroborated standing water beneath cloud cover.',
    },
    {
      id: 'QRY-8840-SI',
      query: 'Which regions show vegetation stress and where has crop health decreased?',
      mode: 'single',
      modeLabel: 'Single Image VQA',
      timestamp: '2026-08-24 12:18:55',
      confidence: 0.846,
      latencyMs: 290,
      answer: 'NDVI anomalies detected in eastern crop parcels. Mean NDVI dropped from 0.68 to 0.41 indicating acute water stress.',
    },
  ];

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#1c1f2a]/50 via-[#0f131d] to-[#0a0e18]">
      <div className="max-w-5xl mx-auto space-y-6 pb-12">
        {/* Header */}
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-end border-b border-white/10 pb-4 gap-4">
          <div>
            <div className="font-['JetBrains_Mono'] text-xs text-[#00f2ff] mb-1 uppercase tracking-widest">
              Session Archive & Logs
            </div>
            <h2 className="font-['Geist',sans-serif] text-3xl font-bold text-[#dfe2f1]">
              Query Execution History
            </h2>
          </div>

          {onClearHistory && (
            <button
              onClick={onClearHistory}
              className="px-3 py-1.5 rounded-lg bg-[#313540] hover:bg-[#ffb4ab]/20 text-[#ffb4ab] text-xs font-['JetBrains_Mono'] border border-white/10 transition-colors"
            >
              Clear Session Logs
            </button>
          )}
        </header>

        {/* History List */}
        <div className="space-y-4">
          {sampleHistory.map((item) => (
            <div
              key={item.id}
              className="glass-panel rounded-xl p-5 bg-[#171b26]/80 border border-white/10 hover:border-[#00f2ff]/40 transition-all flex flex-col md:flex-row justify-between items-start md:items-center gap-4"
            >
              <div className="space-y-2 flex-1">
                <div className="flex items-center gap-3">
                  <span className="font-['JetBrains_Mono'] text-xs font-bold text-[#00f2ff]">
                    {item.id}
                  </span>
                  <span className="px-2 py-0.5 rounded-full bg-[#0566d9]/20 border border-[#0566d9]/40 text-[#adc6ff] text-[10px] font-['JetBrains_Mono']">
                    {item.modeLabel}
                  </span>
                  <span className="text-[11px] font-['JetBrains_Mono'] text-[#849495]">
                    {item.timestamp}
                  </span>
                  <span className="text-[11px] font-['JetBrains_Mono'] text-[#74f5ff]">
                    {item.latencyMs}ms
                  </span>
                </div>

                <div className="text-sm font-semibold text-[#dfe2f1] font-['Inter']">
                  "{item.query}"
                </div>

                <div className="text-xs text-[#b9cacb] font-['Inter'] line-clamp-2">
                  {item.answer}
                </div>
              </div>

              {/* Confidence Badge & Replay CTA */}
              <div className="flex items-center gap-4 shrink-0">
                <div className="text-right">
                  <div className="text-[10px] font-['JetBrains_Mono'] text-[#849495] uppercase">Confidence</div>
                  <div className="text-lg font-bold text-[#00f2ff] font-['Geist',sans-serif]">
                    {Math.round(item.confidence * 100)}%
                  </div>
                </div>

                <button
                  onClick={() => onReplayQuery && onReplayQuery(item)}
                  className="px-4 py-2 rounded-lg bg-[#00f2ff]/15 hover:bg-[#00f2ff]/25 text-[#00f2ff] border border-[#00f2ff]/30 font-['JetBrains_Mono'] text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer"
                >
                  <span className="material-symbols-outlined text-[16px]">replay</span>
                  <span>Replay</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
