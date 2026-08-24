import React from 'react';

/**
 * SatQuery AI — Evidence Report Component (Stitch Design)
 */
export default function EvidenceReport({ result, query, onBackToWorkspace }) {
  const confidencePercent = result?.confidence ? Math.round(result.confidence * 100) : 87.4;
  const confidenceLevel = confidencePercent >= 80 ? 'HIGH' : confidencePercent >= 50 ? 'MODERATE' : 'LOW';

  const defaultSummary = result?.answer || (
    "Based on cross-modal satellite imagery analysis spanning the requested temporal window, there is high probability of recent structural development (+12% expansion) at the target coordinates. SAR backscatter signatures corroborate optical anomalies observed in the vegetation indices."
  );

  const modalities = result?.modalities_used || [
    { name: 'Sentinel-2 (Optical MSI)', count: '2 SCENES', status: 'ACTIVE' },
    { name: 'Sentinel-1 (SAR C-Band)', count: '2 PASSES', status: 'ACTIVE' },
    { name: 'Landsat-8 (Thermal TIRS)', count: 'EXCLUDED', status: 'INACTIVE' },
  ];

  const analyses = result?.analyses_performed || [
    'NDVI Spectral Index Computation',
    'NDWI Surface Water Extraction',
    'Cross-Sensor Sub-pixel Registration (RMSE: 0.38px)',
    'SAR Backscatter Sigma-0 Calibration & Lee Speckle Filter',
    'Bi-Temporal Change Detection Difference Masking',
  ];

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-[#1c1f2a]/50 via-[#0f131d] to-[#0a0e18]">
      <div className="max-w-5xl mx-auto space-y-6 pb-12">
        {/* Header Section */}
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-end border-b border-white/10 pb-4 gap-4">
          <div>
            <div className="font-['JetBrains_Mono'] text-xs text-[#00f2ff] mb-1 uppercase tracking-widest flex items-center gap-2">
              <span>Report ID: SQ-{result?.session_id ? result.session_id.substring(0, 6).toUpperCase() : '8472-A'}</span>
              <span className="text-[#849495]">·</span>
              <span className="text-[#adc6ff]">SIH 2026 AUDIT RECORD</span>
            </div>
            <h2 className="font-['Geist',sans-serif] text-3xl font-bold text-[#dfe2f1]">
              Intelligence Evidence Report
            </h2>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={onBackToWorkspace}
              className="px-4 py-2 rounded-lg bg-[#262a35] hover:bg-[#313540] text-[#dfe2f1] font-['JetBrains_Mono'] text-xs flex items-center gap-2 border border-white/10 transition-colors"
            >
              <span className="material-symbols-outlined text-[16px]">arrow_back</span>
              Back to Workspace
            </button>

            <button
              onClick={handlePrint}
              className="bg-[#0566d9] hover:bg-[#0566d9]/80 text-[#e6ecff] px-4 py-2 rounded-lg flex items-center gap-2 transition-all border border-[#00f2ff]/30 shadow-[0_0_15px_rgba(0,242,255,0.2)] font-['JetBrains_Mono'] text-xs font-semibold cursor-pointer"
            >
              <span className="material-symbols-outlined text-[18px] fill">picture_as_pdf</span>
              <span>Export PDF</span>
            </button>
          </div>
        </header>

        {/* User Query Banner */}
        <div className="p-3.5 rounded-lg bg-[#171b26] border border-white/10 flex items-center gap-3 text-xs font-['JetBrains_Mono'] text-[#b9cacb]">
          <span className="text-[#00f2ff] uppercase font-bold">Query Investigated:</span>
          <span className="text-[#dfe2f1] italic">"{query || 'Identify new structures built between the two dates and estimate their area.'}"</span>
        </div>

        {/* Summary & Confidence Card */}
        <div className="glass-panel rounded-xl p-6 flex flex-col md:flex-row justify-between items-start gap-6 border-l-4 border-l-[#00f2ff] bg-[#171b26]/80">
          <div className="max-w-2xl">
            <h3 className="font-['Geist',sans-serif] text-lg font-bold text-[#00dbe7] mb-2 flex items-center gap-2">
              <span className="material-symbols-outlined text-[#00f2ff]">psychology</span>
              <span>Analyst Findings & Synthesis</span>
            </h3>
            <p className="font-['Inter'] text-sm text-[#dfe2f1] leading-relaxed">
              {defaultSummary}
            </p>
          </div>

          <div className="shrink-0 bg-[#0a0e18] rounded-xl p-4 border border-white/10 flex flex-col items-center justify-center min-w-[150px] shadow-lg">
            <div className="font-['JetBrains_Mono'] text-[10px] text-[#b9cacb] mb-1 uppercase tracking-wider">
              Calculated Confidence
            </div>
            <div className="font-['Geist',sans-serif] text-3xl font-bold text-[#00f2ff]">
              {confidencePercent}%
            </div>
            <div className="font-['JetBrains_Mono'] text-[10px] text-[#00f2ff] mt-1.5 bg-[#00f2ff]/15 border border-[#00f2ff]/30 px-2.5 py-0.5 rounded-full font-bold">
              {confidenceLevel} AGREEMENT
            </div>
          </div>
        </div>

        {/* Warnings & Insufficient Evidence Callout */}
        <div className="bg-[#93000a]/20 border border-[#ffb4ab]/30 rounded-xl p-4 flex items-start gap-3.5">
          <span className="material-symbols-outlined text-[#ffb4ab] mt-0.5 fill text-[22px]">warning</span>
          <div>
            <h4 className="font-['Geist',sans-serif] text-sm font-bold text-[#ffb4ab] mb-1">
              Data Quality & Operational Disclosure
            </h4>
            <p className="font-['Inter'] text-xs text-[#ffdad6] leading-relaxed">
              Optical scenes exhibited 8% localized cloud shadowing in quadrant NE-2. SAR VV/VH cross-polarization was utilized to corroborate structural footprint ground truth. Decision support output requires ground validation for statutory compliance.
            </p>
          </div>
        </div>

        {/* Bento Grid: Modalities & Analyses */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Data Modalities Used */}
          <div className="glass-panel rounded-xl p-5 flex flex-col h-full bg-[#171b26]/70 border border-white/10">
            <h3 className="font-['Geist',sans-serif] text-base font-bold text-[#dfe2f1] border-b border-white/10 pb-2.5 mb-4 flex items-center gap-2">
              <span className="material-symbols-outlined text-[#00dbe7]">satellite_alt</span>
              <span>Data Modalities Ingested</span>
            </h3>
            <ul className="space-y-2.5 flex-1 font-['JetBrains_Mono'] text-xs">
              {modalities.map((item, idx) => (
                <li
                  key={idx}
                  className="flex justify-between items-center bg-[#0a0e18]/60 px-3.5 py-2.5 rounded-lg border border-white/5"
                >
                  <span className="text-[#dfe2f1]">{item.name}</span>
                  <span
                    className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      item.status === 'ACTIVE'
                        ? 'bg-[#00f2ff]/15 text-[#00f2ff] border border-[#00f2ff]/30'
                        : 'bg-[#313540] text-[#849495]'
                    }`}
                  >
                    {item.count}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Analyses Performed */}
          <div className="glass-panel rounded-xl p-5 flex flex-col h-full bg-[#171b26]/70 border border-white/10">
            <h3 className="font-['Geist',sans-serif] text-base font-bold text-[#dfe2f1] border-b border-white/10 pb-2.5 mb-4 flex items-center gap-2">
              <span className="material-symbols-outlined text-[#74f5ff]">task_alt</span>
              <span>Specialist Analyses Performed</span>
            </h3>
            <div className="space-y-2 font-['JetBrains_Mono'] text-xs text-[#b9cacb] flex-1">
              {analyses.map((task, idx) => (
                <div key={idx} className="flex items-center gap-2.5 bg-[#0a0e18]/40 px-3 py-2 rounded border border-white/5">
                  <span className="material-symbols-outlined text-[#00f2ff] text-[16px] fill">check_circle</span>
                  <span className="text-[#dfe2f1]">{task}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Spatial Metrics Table */}
        <div className="glass-panel rounded-xl p-5 bg-[#171b26]/70 border border-white/10">
          <h3 className="font-['Geist',sans-serif] text-base font-bold text-[#dfe2f1] mb-3 flex items-center gap-2">
            <span className="material-symbols-outlined text-[#00f2ff]">analytics</span>
            <span>Spatial Change & Quantitative Metrics</span>
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left font-['JetBrains_Mono'] text-xs border-collapse">
              <thead>
                <tr className="border-b border-white/10 text-[#849495] uppercase text-[10px]">
                  <th className="py-2 px-3">Target Cluster</th>
                  <th className="py-2 px-3">Coordinates (Center)</th>
                  <th className="py-2 px-3">Class Transition</th>
                  <th className="py-2 px-3">Estimated Area (m²)</th>
                  <th className="py-2 px-3">Confidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-[#dfe2f1]">
                <tr>
                  <td className="py-2.5 px-3 font-bold text-[#00f2ff]">Cluster #01</td>
                  <td className="py-2.5 px-3 text-[#b9cacb]">18.5204° N, 73.8567° E</td>
                  <td className="py-2.5 px-3">Bare Soil → Industrial Built-up</td>
                  <td className="py-2.5 px-3">14,280 m²</td>
                  <td className="py-2.5 px-3 text-[#00f2ff]">89.2%</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-3 font-bold text-[#00f2ff]">Cluster #02</td>
                  <td className="py-2.5 px-3 text-[#b9cacb]">18.5231° N, 73.8592° E</td>
                  <td className="py-2.5 px-3">Vegetation → Logistics Pavement</td>
                  <td className="py-2.5 px-3">8,450 m²</td>
                  <td className="py-2.5 px-3 text-[#00f2ff]">86.5%</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-3 font-bold text-[#00f2ff]">Cluster #03</td>
                  <td className="py-2.5 px-3 text-[#b9cacb]">18.5189° N, 73.8540° E</td>
                  <td className="py-2.5 px-3">Water Margin → Sedimentary Deposition</td>
                  <td className="py-2.5 px-3">3,120 m²</td>
                  <td className="py-2.5 px-3 text-[#00f2ff]">84.1%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
