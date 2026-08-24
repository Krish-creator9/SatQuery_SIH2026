import React from 'react';

/**
 * SatQuery AI — Top Navigation Bar (Stitch Design Component)
 */
export default function TopNavBar({ activeTab, queryId, backendStatus, onOpenSettings, onOpenNotifications }) {
  const getTabTitle = () => {
    switch (activeTab) {
      case 'single': return 'Single Image Analysis';
      case 'change': return 'Change Detection Analysis';
      case 'fusion': return 'Optical + SAR Fusion';
      case 'scenarios': return 'Mission Scenarios';
      case 'report': return 'Intelligence Evidence Report';
      case 'trace': return 'Agent Execution Trace';
      case 'history': return 'Query History & Telemetry';
      case 'about': return 'Architecture & Specifications';
      default: return 'Mission Control';
    }
  };

  return (
    <header className="h-[64px] bg-[#0f131d]/80 backdrop-blur-xl border-b border-white/10 px-6 flex items-center justify-between sticky top-0 z-50 w-full select-none">
      {/* Brand & Mode Context */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full border border-[#00f2ff]/40 bg-[#1c1f2a] flex items-center justify-center p-1 glow-cyan">
            <span className="material-symbols-outlined text-[#00f2ff] text-[20px] fill">satellite_alt</span>
          </div>
          <div>
            <div className="font-['Geist',sans-serif] font-bold text-lg text-[#00dbe7] tracking-tight flex items-center gap-2">
              SatQuery AI
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#00f2ff]/10 text-[#00f2ff] border border-[#00f2ff]/30 font-['JetBrains_Mono']">
                SIH 2026
              </span>
            </div>
            <div className="text-[11px] text-[#b9cacb] font-['JetBrains_Mono'] uppercase tracking-wider flex items-center gap-1.5">
              <span>{getTabTitle()}</span>
              {queryId && (
                <>
                  <span className="text-[#849495]">·</span>
                  <span className="text-[#00f2ff]">{queryId}</span>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Status & Actions */}
      <div className="flex items-center gap-4">
        {/* Backend Status Indicator */}
        <div className="px-3 py-1 rounded-full bg-[#1c1f2a] border border-white/10 text-[#adc6ff] font-['JetBrains_Mono'] text-[11px] flex items-center gap-2">
          <span
            className={`w-2 h-2 rounded-full ${
              backendStatus === 'healthy'
                ? 'bg-[#00f2ff] animate-pulse shadow-[0_0_8px_#00f2ff]'
                : backendStatus === 'checking'
                ? 'bg-[#fc8f34] animate-ping'
                : 'bg-[#ffb4ab]'
            }`}
          />
          <span className="hidden sm:inline">
            {backendStatus === 'healthy' ? 'SYSTEM: ONLINE' : backendStatus === 'checking' ? 'CONNECTING...' : 'OFFLINE'}
          </span>
        </div>

        {/* Action Icons */}
        <button
          onClick={onOpenNotifications}
          title="Notifications"
          className="w-9 h-9 rounded-full bg-[#1c1f2a]/60 hover:bg-[#313540] text-[#b9cacb] hover:text-[#00f2ff] border border-white/5 transition-all flex items-center justify-center cursor-pointer active:scale-95"
        >
          <span className="material-symbols-outlined text-[18px]">notifications</span>
        </button>

        <button
          onClick={onOpenSettings}
          title="Settings"
          className="w-9 h-9 rounded-full bg-[#1c1f2a]/60 hover:bg-[#313540] text-[#b9cacb] hover:text-[#00f2ff] border border-white/5 transition-all flex items-center justify-center cursor-pointer active:scale-95"
        >
          <span className="material-symbols-outlined text-[18px]">settings</span>
        </button>

        {/* User Agent Avatar */}
        <div className="w-8 h-8 rounded-full bg-[#1c1f2a] border border-[#00dbe7]/50 overflow-hidden ml-1 cursor-pointer hover:border-[#00f2ff] transition-colors">
          <img
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuAQ1KzTgAPLodPHnjPrSMaWqQNhXfTNXv8Zn7RFs-lV6vD5uRs15wq-q9HXK2IXlFOaj5vn0WVWBI-L_MlMSqGlC191GVNZ57Ey9E7HEB-GBf2ILHWMD-9XATdaFXeEJL0zsgDTlYaDhZZVbsCZQOsi1CzPmHzkb-PiitFE8i4jb4IhV2CThJU6oWfuA2w-dXSDs2a_D7GoiNZJL4xsTMb6e4Hrcy3itSHmphJPXZfgOUoONVH8_S7F"
            alt="Mission Operative"
            className="w-full h-full object-cover"
          />
        </div>
      </div>
    </header>
  );
}
