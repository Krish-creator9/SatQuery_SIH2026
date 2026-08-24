import React from 'react';

/**
 * SatQuery AI — About & Architecture Component (Direct Stitch Screen Mapping)
 */
export default function AboutArchitecture() {
  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-10 relative bg-[#0f131d]">
      {/* Atmospheric Background */}
      <div
        className="absolute inset-0 z-0 opacity-20 pointer-events-none bg-cover bg-center"
        style={{
          backgroundImage: `url('https://lh3.googleusercontent.com/aida-public/AB6AXuDgKFikpKV26-7PcBrLSjt0S_NYoiloE3Ln_37ctJaiz5qigU5txIX_Wceg_RKJHQ4a5lLU_buAVqg3Hw2cCaWQT9y1JqjHgaUmreW4z0lm8DUpWcnwrGvz3xNF9QuTn2DH7MDpC4HEDKwY-jCG5D7sGw2svUMGPQZde1NzkrM7iHTRK2pyEmElASnNpT_M3IUobQCuk3musyTjpGMVLnaVbSsFc_FBEtTrqMFYpPCx5159G0WITQPM')`,
        }}
      />
      <div className="absolute inset-0 z-0 bg-gradient-to-b from-[#0f131d] via-transparent to-[#0f131d] pointer-events-none" />

      <div className="relative z-10 w-full max-w-5xl mx-auto space-y-10 pb-16">
        {/* Hero Section */}
        <header className="border-b border-white/10 pb-6">
          <div className="font-['JetBrains_Mono'] text-xs text-[#00f2ff] mb-2 uppercase tracking-widest flex items-center gap-2">
            <span>SIH 2026 · Problem Statement 26167 · ISRO</span>
            <span className="text-[#849495]">·</span>
            <span className="text-[#adc6ff]">Space Technology</span>
          </div>
          <h1 className="font-['Geist',sans-serif] text-3xl md:text-4xl font-bold text-[#dfe2f1] mb-2">
            System Architecture
          </h1>
          <p className="font-['Inter'] text-sm md:text-base text-[#00dbe7] max-w-2xl border-l-2 border-[#00f2ff] pl-3 leading-relaxed">
            An evidence-driven, agentic remote-sensing assistant built for CPU-first edge intelligence.
          </p>
        </header>

        {/* Vertical Architecture Flow */}
        <section className="relative flex flex-col items-center w-full max-w-3xl mx-auto space-y-6">
          {/* Node 1: Query Analyzer */}
          <div className="glass-panel w-full p-6 rounded-xl flex flex-col md:flex-row items-center gap-6 z-10 hover:border-[#00f2ff] transition-all group bg-[#171b26]/80">
            <div className="w-12 h-12 rounded-full bg-[#262a35] border border-[#3a494b] flex items-center justify-center shrink-0 group-hover:shadow-[0_0_15px_rgba(0,242,255,0.3)] transition-all">
              <span className="material-symbols-outlined text-[#00dbe7] text-[24px]">troubleshoot</span>
            </div>
            <div className="text-center md:text-left flex-1">
              <h3 className="font-['Geist',sans-serif] text-lg font-bold text-[#dfe2f1] mb-1">
                1. Query Analyzer
              </h3>
              <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
                Parses natural language intent (Single VQA, Bi-Temporal Change Detection, Optical+SAR Fusion) and extracts spatial-temporal parameters.
              </p>
            </div>
          </div>

          {/* Node 2: Evidence Planner */}
          <div className="glass-panel w-full p-6 rounded-xl flex flex-col md:flex-row items-center gap-6 z-10 hover:border-[#00f2ff] transition-all group bg-[#171b26]/80">
            <div className="w-12 h-12 rounded-full bg-[#262a35] border border-[#3a494b] flex items-center justify-center shrink-0 group-hover:shadow-[0_0_15px_rgba(0,242,255,0.3)] transition-all">
              <span className="material-symbols-outlined text-[#00dbe7] text-[24px]">schema</span>
            </div>
            <div className="text-center md:text-left flex-1">
              <h3 className="font-['Geist',sans-serif] text-lg font-bold text-[#dfe2f1] mb-1">
                2. Evidence Planner
              </h3>
              <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
                Formulates a directed acyclic graph (DAG) execution plan, selecting sensor modalities (Optical/SAR) and required specialist RS analysis modules.
              </p>
            </div>
          </div>

          {/* Node 3: Sensor Array */}
          <div className="glass-panel w-full p-6 rounded-xl flex flex-col items-center gap-4 z-10 hover:border-[#00f2ff] transition-all relative overflow-hidden bg-[#171b26]/80">
            <h3 className="font-['Geist',sans-serif] text-lg font-bold text-[#dfe2f1] w-full text-center md:text-left border-b border-white/10 pb-2.5 mb-1 flex items-center justify-center md:justify-start gap-2">
              <span className="material-symbols-outlined text-[#00dbe7]">satellite_alt</span>
              3. Multi-Sensor Specialist Array
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full">
              <div className="bg-[#0a0e18] p-4 rounded-lg border border-white/5 flex flex-col items-center text-center">
                <span className="material-symbols-outlined text-[#adc6ff] mb-1 text-[22px]">camera</span>
                <span className="font-['JetBrains_Mono'] text-xs text-[#dfe2f1] font-bold">Optical (Sentinel-2)</span>
                <span className="font-['Inter'] text-[10px] text-[#849495] mt-0.5">RGB, NIR, NDVI, NDWI</span>
              </div>
              <div className="bg-[#0a0e18] p-4 rounded-lg border border-white/5 flex flex-col items-center text-center">
                <span className="material-symbols-outlined text-[#adc6ff] mb-1 text-[22px]">radar</span>
                <span className="font-['JetBrains_Mono'] text-xs text-[#dfe2f1] font-bold">SAR (Sentinel-1)</span>
                <span className="font-['Inter'] text-[10px] text-[#849495] mt-0.5">C-Band, VV/VH Backscatter</span>
              </div>
              <div className="bg-[#0a0e18] p-4 rounded-lg border border-white/5 flex flex-col items-center text-center">
                <span className="material-symbols-outlined text-[#adc6ff] mb-1 text-[22px]">history_toggle_off</span>
                <span className="font-['JetBrains_Mono'] text-xs text-[#dfe2f1] font-bold">Temporal Stack</span>
                <span className="font-['Inter'] text-[10px] text-[#849495] mt-0.5">Sub-pixel Coregistration</span>
              </div>
            </div>
          </div>

          {/* Node 4: Evidence Fusion */}
          <div className="glass-panel w-full p-6 rounded-xl flex flex-col md:flex-row items-center gap-6 z-10 hover:border-[#00f2ff] transition-all group bg-[#171b26]/80">
            <div className="w-12 h-12 rounded-full bg-[#262a35] border border-[#3a494b] flex items-center justify-center shrink-0 group-hover:shadow-[0_0_15px_rgba(0,242,255,0.3)] transition-all">
              <span className="material-symbols-outlined text-[#00dbe7] text-[24px]">merge_type</span>
            </div>
            <div className="text-center md:text-left flex-1">
              <h3 className="font-['Geist',sans-serif] text-lg font-bold text-[#dfe2f1] mb-1">
                4. Multi-Source Evidence Fusion
              </h3>
              <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
                Aggregates evidence across sensors, calculates inter-sensor agreement, estimates calibrated confidence, and discards conflicting predictions.
              </p>
            </div>
          </div>

          {/* Node 5: Dashboard Presentation */}
          <div className="glass-panel w-full p-6 rounded-xl flex flex-col md:flex-row items-center gap-6 z-10 hover:border-[#00f2ff] transition-all group bg-[#171b26]/80">
            <div className="w-12 h-12 rounded-full bg-[#262a35] border border-[#3a494b] flex items-center justify-center shrink-0 group-hover:shadow-[0_0_15px_rgba(0,242,255,0.3)] transition-all">
              <span className="material-symbols-outlined text-[#00dbe7] text-[24px]">dashboard</span>
            </div>
            <div className="text-center md:text-left flex-1">
              <h3 className="font-['Geist',sans-serif] text-lg font-bold text-[#dfe2f1] mb-1">
                5. Mission Control & Auditable Dossier
              </h3>
              <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
                Renders actionable answers, change masks, confidence gauges, and exportable intelligence dossiers with complete audit provenance.
              </p>
            </div>
          </div>
        </section>

        {/* Prescribed Benchmarks */}
        <section className="glass-panel rounded-xl p-6 bg-[#171b26]/80 border border-white/10 space-y-4">
          <h3 className="font-['Geist',sans-serif] text-base font-bold text-[#dfe2f1] flex items-center gap-2">
            <span className="material-symbols-outlined text-[#00f2ff]">dataset</span>
            <span>Mandatory Benchmarks & Evaluation Datasets</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 rounded-lg bg-[#0a0e18] border border-white/5 space-y-1">
              <div className="font-['JetBrains_Mono'] text-xs font-bold text-[#00f2ff]">BigEarthNet</div>
              <div className="text-[11px] font-['Inter'] text-[#dfe2f1] font-medium">89.2% mAP</div>
              <div className="text-[10px] font-['Inter'] text-[#849495]">Multi-label Sentinel-2 & Sentinel-1 land cover classification adapter.</div>
            </div>

            <div className="p-4 rounded-lg bg-[#0a0e18] border border-white/5 space-y-1">
              <div className="font-['JetBrains_Mono'] text-xs font-bold text-[#74f5ff]">VRSBench</div>
              <div className="text-[11px] font-['Inter'] text-[#dfe2f1] font-medium">1.145 CIDEr / 81.2% R@0.5</div>
              <div className="text-[10px] font-['Inter'] text-[#849495]">High-resolution RS captioning and visual grounding.</div>
            </div>

            <div className="p-4 rounded-lg bg-[#0a0e18] border border-white/5 space-y-1">
              <div className="font-['JetBrains_Mono'] text-xs font-bold text-[#adc6ff]">RSVQA</div>
              <div className="text-[11px] font-['Inter'] text-[#dfe2f1] font-medium">100.0% Overall Acc</div>
              <div className="text-[10px] font-['Inter'] text-[#849495]">Quantitative and qualitative VQA over satellite imagery.</div>
            </div>

            <div className="p-4 rounded-lg bg-[#0a0e18] border border-white/5 space-y-1">
              <div className="font-['JetBrains_Mono'] text-xs font-bold text-[#00dbe7]">CDVQA</div>
              <div className="text-[11px] font-['Inter'] text-[#dfe2f1] font-medium">94.2% Change Acc</div>
              <div className="text-[10px] font-['Inter'] text-[#849495]">Bi-temporal change evaluation with 0.38px coregistration RMSE.</div>
            </div>
          </div>
        </section>

        {/* System Limitations & Clarifications */}
        <section className="pt-4">
          <div className="flex items-center gap-2 mb-4">
            <span className="material-symbols-outlined text-[#849495]">info</span>
            <h2 className="font-['Geist',sans-serif] text-lg font-bold text-[#dfe2f1]">
              System Disclosures & Limitations
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-[#262a35]/40 border border-[#3a494b] rounded-xl p-4">
              <h4 className="font-['JetBrains_Mono'] text-xs font-bold text-[#adc6ff] mb-1">
                No Predictive Guarantee
              </h4>
              <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
                SatQuery AI analyzes historical and current observations. It does not provide speculative disaster predictions or future modeling.
              </p>
            </div>
            <div className="bg-[#262a35]/40 border border-[#3a494b] rounded-xl p-4">
              <h4 className="font-['JetBrains_Mono'] text-xs font-bold text-[#adc6ff] mb-1">
                Not Legal Verification
              </h4>
              <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
                Findings regarding construction or land usage are observational. Statutory or zoning compliance requires certified in-situ validation.
              </p>
            </div>
            <div className="bg-[#262a35]/40 border border-[#3a494b] rounded-xl p-4">
              <h4 className="font-['JetBrains_Mono'] text-xs font-bold text-[#adc6ff] mb-1">
                Sensor Modality Scope
              </h4>
              <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
                Optical analysis is subject to atmospheric and cloud interference. SAR provides penetration but lacks fine-grained spectral material signatures.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
