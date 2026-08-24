import React, { useState } from 'react';

/**
 * SatQuery AI — Analysis Workspace Component (Stitch Mission Control)
 */
export default function AnalysisWorkspace({
  activeTab,
  images,
  onUpload,
  query,
  setQuery,
  onRunQuery,
  loading,
  result,
  onNavigateToReport,
  onNavigateToTrace,
}) {
  const [showMask, setShowMask] = useState(true);
  const [selectedOverlay, setSelectedOverlay] = useState('change'); // 'change', 'ndvi', 'ndwi', 'sar'
  const [activeZone, setActiveZone] = useState('a');

  // Preset query suggestions based on mode
  const suggestions = {
    single: [
      'What type of terrain or land cover is present in this scene?',
      'Identify and highlight all water bodies in this image.',
      'Generate a detailed descriptive caption for this satellite scene.',
    ],
    change: [
      'Identify new structures built between the two dates and estimate their area.',
      'Show areas where water extent increased after the storm.',
      'Has the built-up area increased between these two observations?',
    ],
    fusion: [
      'Perform co-registered optical and SAR analysis to classify surface water.',
      'Compare optical reflectance with SAR backscatter signatures for soil moisture.',
      'Detect structural changes masked by cloud cover in optical imagery.',
    ],
  };

  const currentSuggestions = suggestions[activeTab] || suggestions.change;

  // Placeholder images when no user file is uploaded yet
  const sampleImages = {
    opticalA: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDCFuG4sPEDF1R1BMUAVMK9zwhl5h92_rhW5TYJH43cpv5r_nzixzLA_v9gyFbr6g0oCD8bHAAc2Ety1oNSpY-VYmqhCkYnQbBwXH46rVyblHB0-NpgNlk458sdcPuC7ICMReoPidshxuITvl5bMgp7jm83j4bM7Pftc3zqkZUVlXMmyzufsa_8SdGSa4coFf23547fG6nt2q5Eqy6BV5z8zL72xz69yOA9l1YjmU2lgVq2-9lbdQmw',
    opticalB: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCzXL9Ul21OAiOy8jijW1207kzDgRCuVETAQeJkE64AgMIFEX8Ez_br7id0s4InUxA04XZ48gQfkIX4cbqFNwF99Z0UjFry7Jei036MZTTtPnXWCTV4k0Eivt-IDvmJjqTMgCySozQ3C1vf3PwvAg-IrVZr7RYMcw3gkYNW1n-uRafQf-u7Y6dL-HcEwdkOD8ykNvGBrZATnKyIjx2LENTgqfYQ0G75E-4YJZn9QCC77Zz1iv9G_BzF',
    sar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD85e7knO2UVkLhaZDcFt_tZgOSaSkuRp7Cal9bwYZbBZLx8UMPu2vJf5uUR9QtmCIdQk__k95vis5yFQN0FseOCxH6LIQsD_UACbbtBJO7DeQ_A0di0vgep1Qwup_FsJQPC0F1EqfoMuWP6aj8vxJzHkPKrHuvQ11km2KW4cMjYE_dOEF9kxKqQWb2TCKYizKIPTCyrwISInnAVd-0m3aHwoRpt8Lqu_UukNJYbEt9iSzdf3_R4pok',
  };

  const imgAUrl = images[0]?.preview || sampleImages.opticalA;
  const imgBUrl = images[1]?.preview || (activeTab === 'fusion' ? sampleImages.sar : sampleImages.opticalB);

  return (
    <div className="flex-1 flex overflow-hidden h-[calc(100vh-64px)] bg-[#0a0e18]">
      {/* Center Workspace */}
      <main className="flex-1 flex flex-col relative z-0 overflow-y-auto p-6 gap-6 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#1c1f2a]/40 via-[#0a0e18] to-[#0a0e18]">
        {/* Workspace Header */}
        <div className="flex justify-between items-end">
          <div>
            <h1 className="font-['Geist',sans-serif] text-2xl font-bold text-[#dfe2f1]">
              {activeTab === 'single'
                ? 'Single Image Multimodal Analysis'
                : activeTab === 'fusion'
                ? 'Optical + SAR Co-Registered Fusion'
                : 'Bi-Temporal Change Detection Analysis'}
            </h1>
            <p className="text-sm text-[#b9cacb] mt-1 font-['Inter']">
              {activeTab === 'single'
                ? 'Extract spectral indices, ground objects, and perform VQA over single scenes.'
                : activeTab === 'fusion'
                ? 'Combine optical spectral reflectance with SAR backscatter radar structure.'
                : 'Upload or select baseline and target observations to identify structural and environmental change.'}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full bg-[#0566d9]/20 border border-[#0566d9]/50 text-[#adc6ff] font-['JetBrains_Mono'] text-[11px] flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#00f2ff] animate-pulse"></span>
              AGENT READY
            </span>
          </div>
        </div>

        {/* Upload & Imagery Zones Grid */}
        <div className={`grid ${activeTab === 'single' ? 'grid-cols-1' : 'grid-cols-2'} gap-6 flex-1 min-h-[380px]`}>
          {/* Zone A */}
          <div className="glass-panel rounded-xl flex flex-col overflow-hidden group border border-white/10">
            <div className="px-4 py-2.5 border-b border-white/10 flex justify-between items-center bg-[#262a35]/40">
              <div className="font-['JetBrains_Mono'] text-xs text-[#dfe2f1] flex items-center gap-2">
                <span className="material-symbols-outlined text-[16px] text-[#00dbe7]">satellite_alt</span>
                <span>{activeTab === 'fusion' ? 'Sentinel-2 (Optical MSI)' : 'Observation A — Baseline (2020)'}</span>
              </div>
              <label className="text-[11px] font-['JetBrains_Mono'] text-[#00f2ff] hover:underline cursor-pointer">
                Upload Custom
                <input
                  type="file"
                  accept=".tif,.tiff,.png,.jpg,.jpeg"
                  className="hidden"
                  onChange={(e) => e.target.files?.[0] && onUpload(e.target.files[0], 'optical', 'primary')}
                />
              </label>
            </div>

            <div className="flex-1 p-4 flex flex-col relative bg-[#0f131d]/60">
              <div className="w-full h-full rounded-lg border border-white/10 overflow-hidden relative group-hover:border-[#00f2ff]/40 transition-colors">
                <img
                  src={imgAUrl}
                  alt="Observation A"
                  className="w-full h-full object-cover opacity-85 hover:opacity-100 transition-opacity"
                />
                <div className="absolute top-3 right-3 flex gap-2">
                  <span className="bg-[#0f131d]/85 backdrop-blur-sm border border-white/10 px-2 py-0.5 rounded font-['JetBrains_Mono'] text-[10px] text-[#00dbe7]">
                    OPTICAL 4-BAND
                  </span>
                  <span className="bg-[#0f131d]/85 backdrop-blur-sm border border-white/10 px-2 py-0.5 rounded font-['JetBrains_Mono'] text-[10px] text-[#b9cacb]">
                    0.5m GSD
                  </span>
                </div>
                <div className="absolute bottom-3 left-3 bg-[#0f131d]/90 backdrop-blur px-2.5 py-1 rounded border border-white/10 text-[10px] font-['JetBrains_Mono'] text-[#dfe2f1]">
                  LAT: 18.5204° N · LON: 73.8567° E
                </div>
              </div>
            </div>
          </div>

          {/* Zone B (if Change or Fusion) */}
          {activeTab !== 'single' && (
            <div className="glass-panel rounded-xl flex flex-col overflow-hidden group border border-white/10">
              <div className="px-4 py-2.5 border-b border-white/10 flex justify-between items-center bg-[#262a35]/40">
                <div className="font-['JetBrains_Mono'] text-xs text-[#dfe2f1] flex items-center gap-2">
                  <span className="material-symbols-outlined text-[16px] text-[#adc6ff]">
                    {activeTab === 'fusion' ? 'radar' : 'satellite_alt'}
                  </span>
                  <span>{activeTab === 'fusion' ? 'Sentinel-1 (SAR C-Band)' : 'Observation B — Target (2024)'}</span>
                </div>
                <label className="text-[11px] font-['JetBrains_Mono'] text-[#00f2ff] hover:underline cursor-pointer">
                  Upload Custom
                  <input
                    type="file"
                    accept=".tif,.tiff,.png,.jpg,.jpeg"
                    className="hidden"
                    onChange={(e) => e.target.files?.[0] && onUpload(e.target.files[0], activeTab === 'fusion' ? 'sar' : 'optical', 'secondary')}
                  />
                </label>
              </div>

              <div className="flex-1 p-4 flex flex-col relative bg-[#0f131d]/60">
                <div className="w-full h-full rounded-lg border border-white/10 overflow-hidden relative group-hover:border-[#adc6ff]/40 transition-colors">
                  <img
                    src={imgBUrl}
                    alt="Observation B"
                    className="w-full h-full object-cover opacity-85 hover:opacity-100 transition-opacity"
                  />
                  <div className="absolute top-3 right-3 flex gap-2">
                    <span className="bg-[#0f131d]/85 backdrop-blur-sm border border-white/10 px-2 py-0.5 rounded font-['JetBrains_Mono'] text-[10px] text-[#adc6ff]">
                      {activeTab === 'fusion' ? 'SAR VV/VH' : 'OPTICAL 4-BAND'}
                    </span>
                    <span className="bg-[#0f131d]/85 backdrop-blur-sm border border-white/10 px-2 py-0.5 rounded font-['JetBrains_Mono'] text-[10px] text-[#b9cacb]">
                      {activeTab === 'fusion' ? '10m GSD' : '0.5m GSD'}
                    </span>
                  </div>

                  {/* AI Change / Grounding Overlay Bounding Box */}
                  {showMask && (
                    <div className="absolute top-[28%] left-[38%] w-[130px] h-[90px] border-2 border-[#ffb4ab] border-dashed bg-[#ffb4ab]/15 rounded-sm flex items-start p-1 animate-pulse">
                      <span className="bg-[#93000a]/90 text-[#ffdad6] font-['JetBrains_Mono'] text-[9px] px-1 py-0.5 rounded">
                        NEW_STRUCT +84%
                      </span>
                    </div>
                  )}

                  {/* Change Mask Toggle in image */}
                  <div className="absolute bottom-3 right-3 bg-[#0f131d]/90 backdrop-blur-md px-2.5 py-1 rounded-full border border-white/10 flex items-center gap-2 text-[11px] font-['JetBrains_Mono']">
                    <span>Overlay Mask</span>
                    <button
                      onClick={() => setShowMask(!showMask)}
                      className={`w-8 h-4 rounded-full transition-colors relative ${
                        showMask ? 'bg-[#00f2ff]' : 'bg-[#313540]'
                      }`}
                    >
                      <span
                        className={`w-3 h-3 rounded-full bg-[#0a0e18] absolute top-0.5 transition-transform ${
                          showMask ? 'left-4' : 'left-0.5'
                        }`}
                      />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Suggested Quick Prompt Chips */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs font-['JetBrains_Mono']">
          <span className="text-[#849495] uppercase tracking-wider shrink-0">Quick Prompts:</span>
          {currentSuggestions.map((text, i) => (
            <button
              key={i}
              onClick={() => setQuery(text)}
              className="bg-[#1c1f2a] hover:bg-[#262a35] text-[#dfe2f1] hover:text-[#00f2ff] px-3 py-1.5 rounded-full border border-white/5 shrink-0 transition-colors cursor-pointer text-left truncate max-w-md"
            >
              {text}
            </button>
          ))}
        </div>

        {/* Query Input Bar */}
        <div className="glass-panel rounded-xl p-2 flex items-center gap-3 border border-[#00f2ff]/30 shadow-[0_0_20px_rgba(0,242,255,0.08)] bg-[#171b26]/90">
          <button
            title="Attach dataset or ROI"
            className="p-3 text-[#b9cacb] hover:text-[#00f2ff] rounded-lg hover:bg-[#313540]/60 transition-colors"
          >
            <span className="material-symbols-outlined text-[20px]">attach_file</span>
          </button>

          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                onRunQuery();
              }
            }}
            placeholder="Ask a natural language question about satellite imagery, land change, vegetation health, or SAR backscatter..."
            rows={1}
            className="flex-1 bg-transparent border-none text-[#dfe2f1] font-['Inter'] text-sm placeholder-[#b9cacb]/50 focus:outline-none resize-none py-2"
          />

          <button
            onClick={onRunQuery}
            disabled={loading || !query.trim()}
            className="bg-[#00f2ff]/20 hover:bg-[#00f2ff]/30 text-[#00f2ff] hover:text-white border border-[#00f2ff] px-5 py-2.5 rounded-lg font-['JetBrains_Mono'] text-xs font-semibold flex items-center gap-2 transition-all cursor-pointer active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_12px_rgba(0,242,255,0.2)]"
          >
            {loading ? (
              <>
                <span className="w-3.5 h-3.5 border-2 border-[#00f2ff] border-t-transparent rounded-full animate-spin"></span>
                <span>ANALYZING...</span>
              </>
            ) : (
              <>
                <span>SEND QUERY</span>
                <span className="material-symbols-outlined text-[16px]">send</span>
              </>
            )}
          </button>
        </div>
      </main>

      {/* Right Terminal Execution Trace Sidebar */}
      <aside className="w-[340px] h-full bg-[#0a0e18] border-l border-white/10 flex flex-col shrink-0 select-none z-10">
        {/* Terminal Header */}
        <div className="px-4 py-3 border-b border-white/10 flex justify-between items-center bg-[#171b26]/70">
          <button
            onClick={onNavigateToTrace}
            className="font-['JetBrains_Mono'] text-xs text-[#b9cacb] hover:text-[#00f2ff] flex items-center gap-2 transition-colors w-full"
          >
            <span className="material-symbols-outlined text-[16px] text-[#00f2ff]">terminal</span>
            <span>AGENT EXECUTION TRACE</span>
            <span className="material-symbols-outlined text-[14px] ml-auto">open_in_new</span>
          </button>
        </div>

        {/* Live Terminal Log Stream */}
        <div className="flex-1 overflow-y-auto p-4 font-['JetBrains_Mono'] text-[11px] leading-relaxed flex flex-col gap-2.5 text-[#b9cacb]">
          <div>
            <span className="terminal-prefix-info">[14:02:41 INFO]</span>
            <span className="text-[#dfe2f1]"> System initialization complete. CPU-first pipeline active.</span>
          </div>

          <div>
            <span className="terminal-prefix-info">[14:05:12 RECV]</span>
            <span className="text-[#dfe2f1]"> User query received:</span>
            <div className="text-[#b9cacb] italic pl-2 border-l-2 border-[#313540] ml-1 mt-1 text-[10px]">
              "{query || 'Identify new structures built between the two dates and estimate their area.'}"
            </div>
          </div>

          {/* Intent Parsing Card */}
          <div className="p-2.5 rounded bg-[#000000]/60 border border-white/10 my-1">
            <div className="flex items-center gap-2 mb-1.5">
              <span className="w-2 h-2 rounded-full bg-[#00f2ff] animate-ping"></span>
              <span className="text-[#00dbe7] font-bold">Query Intent & Tool Selection</span>
            </div>
            <div className="pl-3 border-l border-[#00dbe7]/30 ml-1 py-0.5 space-y-0.5 text-[10px]">
              <div>Intent: <span className="text-[#adc6ff]">
                {activeTab === 'single' ? 'SINGLE_VQA_GROUNDING' : activeTab === 'fusion' ? 'OPTICAL_SAR_FUSION' : 'BI_TEMPORAL_CHANGE'}
              </span></div>
              <div>Modality: <span className="text-[#adc6ff]">
                {activeTab === 'fusion' ? 'Sentinel-2 (MSI) + Sentinel-1 (SAR)' : 'Optical Multi-Spectral (RGB+NIR)'}
              </span></div>
              <div>Specialist Engine: <span className="text-[#00f2ff]">
                {activeTab === 'single' ? 'Spectral Indices + Grounding Engine' : activeTab === 'fusion' ? 'SAR Backscatter + Optical Water Engine' : 'Registration + ChangeFormer Diff'}
              </span></div>
            </div>
          </div>

          <div>
            <span className="terminal-prefix-warn">[14:05:15 EXEC]</span>
            <span className="text-[#dfe2f1]"> Coregistering Observation A & B...</span>
          </div>
          <div>
            <span className="terminal-prefix-success">[14:05:18 OK]</span>
            <span className="text-[#dfe2f1]"> Sub-pixel registration aligned. RMSE: 0.38px</span>
          </div>
          <div>
            <span className="terminal-prefix-warn">[14:05:19 EXEC]</span>
            <span className="text-[#dfe2f1]"> Computing normalized difference & feature delta...</span>
          </div>

          {/* Inference Result Pill */}
          <div className="p-2.5 rounded bg-[#000000]/60 border border-white/10 my-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="material-symbols-outlined text-[14px] text-[#00f2ff]">memory</span>
              <span className="text-[#00f2ff] font-bold">Evidence Fusion Complete</span>
            </div>
            <div className="pl-2 text-[10px] space-y-1">
              <div>Detected Variations: <span className="text-[#dfe2f1] font-bold">3 Primary Anomalies</span></div>
              <div>Calibrated Confidence: <span className="text-[#00f2ff] font-bold">
                {result?.confidence ? `${Math.round(result.confidence * 100)}%` : '87.4%'}
              </span></div>
              <div className="mt-2 pt-1 border-t border-white/5">
                <button
                  onClick={onNavigateToReport}
                  className="text-[#00f2ff] hover:underline flex items-center gap-1 font-bold cursor-pointer"
                >
                  View Full Intelligence Report
                  <span className="material-symbols-outlined text-[12px]">arrow_forward</span>
                </button>
              </div>
            </div>
          </div>

          <div className="opacity-75">
            <span className="terminal-prefix-info">[14:05:24 SYNC]</span>
            <span className="text-[#dfe2f1]"> Auditable decision telemetry recorded.</span>
            <span className="inline-block w-1.5 h-3.5 bg-[#00f2ff] ml-1 animate-pulse align-middle"></span>
          </div>
        </div>
      </aside>
    </div>
  );
}
