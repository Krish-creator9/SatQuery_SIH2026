import React from 'react';

/**
 * SatQuery AI — Get Started / Empty State View (Stitch Mission Control)
 */
export default function GetStartedView({ onStartUpload, onExploreScenarios, onLaunchDemo }) {
  return (
    <div className="flex-1 flex items-center justify-center p-8 relative z-10 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-[#1c1f2a]/60 via-[#0f131d] to-[#0a0e18]">
      {/* Central Upload / Action Container */}
      <div className="w-full max-w-2xl glass-panel rounded-2xl p-10 flex flex-col items-center justify-center text-center relative overflow-hidden group border border-white/10 shadow-2xl">
        {/* Animated Dashed SVG Border */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none rounded-2xl">
          <rect
            className="text-[#3a494b] group-hover:text-[#00f2ff]/50 transition-colors duration-500 animated-dash"
            fill="none"
            height="calc(100% - 4px)"
            rx="16"
            ry="16"
            stroke="currentColor"
            strokeWidth="2"
            width="calc(100% - 4px)"
            x="2"
            y="2"
          />
        </svg>

        {/* Logo & Glow */}
        <div className="w-24 h-24 mb-6 relative">
          <div className="absolute inset-0 bg-[#00f2ff]/20 blur-2xl rounded-full scale-150 group-hover:bg-[#00f2ff]/40 transition-colors duration-500" />
          <div className="w-full h-full rounded-2xl bg-[#1c1f2a] border border-[#00f2ff]/40 flex items-center justify-center relative z-10 glow-cyan p-4">
            <span className="material-symbols-outlined text-[#00f2ff] text-[48px] fill">satellite_alt</span>
          </div>
        </div>

        <div className="font-['JetBrains_Mono'] text-xs text-[#00f2ff] uppercase tracking-widest mb-2 font-semibold">
          SIH 2026 · PS 26167 · ISRO
        </div>

        <h2 className="font-['Geist',sans-serif] text-3xl font-bold text-[#dfe2f1] mb-3">
          Welcome to Mission Control
        </h2>
        <p className="font-['Inter'] text-sm text-[#b9cacb] max-w-md mb-8 leading-relaxed">
          Upload satellite imagery (Optical, SAR, or Bi-Temporal pairs) or select an operational scenario to begin AI-assisted multimodal intelligence analysis.
        </p>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center gap-4 w-full justify-center">
          <label className="bg-[#00f2ff]/15 hover:bg-[#00f2ff] text-[#00f2ff] hover:text-[#00363a] border border-[#00f2ff] px-6 py-3 rounded-xl font-['JetBrains_Mono'] text-xs font-bold transition-all duration-300 flex items-center gap-2 glow-hover cursor-pointer active:scale-95 shadow-[0_0_15px_rgba(0,242,255,0.2)]">
            <span className="material-symbols-outlined text-[20px]">cloud_upload</span>
            <span>INITIALIZE UPLOAD</span>
            <input
              type="file"
              accept=".tif,.tiff,.png,.jpg,.jpeg"
              className="hidden"
              onChange={(e) => e.target.files?.[0] && onStartUpload(e.target.files[0])}
            />
          </label>

          <button
            onClick={onExploreScenarios}
            className="bg-[#262a35] hover:bg-[#313540] text-[#dfe2f1] border border-white/10 px-6 py-3 rounded-xl font-['JetBrains_Mono'] text-xs font-semibold transition-all flex items-center gap-2 cursor-pointer active:scale-95"
          >
            <span className="material-symbols-outlined text-[20px]">grid_view</span>
            <span>EXPLORE SCENARIOS</span>
          </button>
        </div>

        <div className="mt-8 flex items-center gap-3">
          <button
            onClick={onLaunchDemo}
            className="text-xs font-['JetBrains_Mono'] text-[#00f2ff] hover:underline flex items-center gap-1 cursor-pointer"
          >
            <span>Or launch preloaded Change Detection demo</span>
            <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
          </button>
        </div>

        <p className="font-['JetBrains_Mono'] text-[11px] text-[#849495] mt-6 tracking-wide uppercase">
          Supported formats: GeoTIFF (.tif, .tiff), JPEG, PNG (Multi-Band & Single-Band)
        </p>
      </div>
    </div>
  );
}
