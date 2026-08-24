import React from 'react';

/**
 * SatQuery AI — Side Navigation Bar (Stitch Design Component)
 */
export default function SideNavBar({ activeTab, onTabChange, queryCount = 0 }) {
  const analysisModes = [
    { id: 'single', label: 'Single Image', icon: 'image', desc: 'VQA, Captioning, Grounding' },
    { id: 'change', label: 'Change Detection', icon: 'compare', desc: 'Bi-temporal Optical Difference' },
    { id: 'fusion', label: 'Optical + SAR Fusion', icon: 'layers', desc: 'Co-registered Joint Analysis' },
    { id: 'scenarios', label: 'Mission Scenarios', icon: 'grid_view', desc: 'Disaster, Agri & Urban Presets' },
  ];

  const intelligenceViews = [
    { id: 'report', label: 'Evidence Report', icon: 'description', desc: 'Analyst Summary & Confidence' },
    { id: 'trace', label: 'Agent Execution Trace', icon: 'account_tree', desc: 'Auditable Decision DAG' },
  ];

  const systemLinks = [
    { id: 'history', label: 'Query History', icon: 'history', badge: queryCount > 0 ? queryCount : null },
    { id: 'about', label: 'About & Architecture', icon: 'info' },
  ];

  return (
    <aside className="w-[280px] h-[calc(100vh-64px)] bg-[#171b26]/90 backdrop-blur-md border-r border-white/10 flex flex-col shrink-0 select-none z-40 overflow-y-auto">
      {/* Analysis Modes Section */}
      <div className="p-4 border-b border-white/10">
        <div className="text-[11px] font-['JetBrains_Mono'] text-[#b9cacb] uppercase tracking-widest mb-3 px-2 flex items-center justify-between">
          <span>Analysis Modes</span>
          <span className="w-1.5 h-1.5 rounded-full bg-[#00f2ff]" />
        </div>
        <div className="flex flex-col gap-1.5">
          {analysisModes.map((mode) => {
            const isActive = activeTab === mode.id;
            return (
              <button
                key={mode.id}
                onClick={() => onTabChange(mode.id)}
                className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center gap-3 transition-all cursor-pointer group ${
                  isActive
                    ? 'bg-[#0566d9]/30 text-[#00f2ff] border-l-4 border-[#00f2ff] shadow-[inset_0_0_12px_rgba(0,242,255,0.15)] font-semibold'
                    : 'text-[#b9cacb] hover:bg-[#313540]/60 hover:text-[#dfe2f1]'
                }`}
              >
                <span
                  className={`material-symbols-outlined text-[20px] transition-colors ${
                    isActive ? 'text-[#00f2ff] fill' : 'text-[#849495] group-hover:text-[#00f2ff]'
                  }`}
                >
                  {mode.icon}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="text-[13px] font-['Geist',sans-serif] truncate">{mode.label}</div>
                  <div className="text-[10px] text-[#849495] truncate font-['Inter']">{mode.desc}</div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Intelligence & Diagnostics Section */}
      <div className="p-4 border-b border-white/10">
        <div className="text-[11px] font-['JetBrains_Mono'] text-[#b9cacb] uppercase tracking-widest mb-3 px-2">
          Intelligence & Trace
        </div>
        <div className="flex flex-col gap-1.5">
          {intelligenceViews.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center gap-3 transition-all cursor-pointer group ${
                  isActive
                    ? 'bg-[#0566d9]/30 text-[#00f2ff] border-l-4 border-[#00f2ff] shadow-[inset_0_0_12px_rgba(0,242,255,0.15)] font-semibold'
                    : 'text-[#b9cacb] hover:bg-[#313540]/60 hover:text-[#dfe2f1]'
                }`}
              >
                <span
                  className={`material-symbols-outlined text-[20px] transition-colors ${
                    isActive ? 'text-[#00f2ff] fill' : 'text-[#849495] group-hover:text-[#00f2ff]'
                  }`}
                >
                  {item.icon}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="text-[13px] font-['Geist',sans-serif] truncate">{item.label}</div>
                  <div className="text-[10px] text-[#849495] truncate font-['Inter']">{item.desc}</div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* System Footer Navigation */}
      <div className="mt-auto p-4 border-t border-white/10 flex flex-col gap-1.5 bg-[#0f131d]/60">
        {systemLinks.map((item) => {
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`w-full text-left px-3 py-2 rounded-lg flex items-center gap-3 transition-all cursor-pointer group ${
                isActive
                  ? 'bg-[#0566d9]/20 text-[#00f2ff] font-medium'
                  : 'text-[#b9cacb] hover:bg-[#313540]/40 hover:text-[#dfe2f1]'
              }`}
            >
              <span
                className={`material-symbols-outlined text-[18px] ${
                  isActive ? 'text-[#00f2ff]' : 'text-[#849495] group-hover:text-[#00f2ff]'
                }`}
              >
                {item.icon}
              </span>
              <span className="text-[12px] font-['JetBrains_Mono'] flex-1 truncate">{item.label}</span>
              {item.badge && (
                <span className="px-1.5 py-0.5 rounded-full bg-[#00f2ff]/20 text-[#00f2ff] text-[10px] font-mono">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </aside>
  );
}
