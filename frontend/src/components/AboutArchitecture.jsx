import React from 'react';

/**
 * SatQuery AI — About & Architecture Component (Stitch Design)
 */
export default function AboutArchitecture() {
  return (
    <div className="flex-1 overflow-y-auto p-8 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#1c1f2a]/50 via-[#0f131d] to-[#0a0e18]">
      <div className="max-w-5xl mx-auto space-y-6 pb-12">
        {/* Header */}
        <header className="border-b border-white/10 pb-4">
          <div className="font-['JetBrains_Mono'] text-xs text-[#00f2ff] mb-1 uppercase tracking-widest flex items-center gap-2">
            <span>SIH 2026 · Problem Statement 26167 · ISRO</span>
            <span className="text-[#849495]">·</span>
            <span className="text-[#adc6ff]">Space Technology</span>
          </div>
          <h2 className="font-['Geist',sans-serif] text-3xl font-bold text-[#dfe2f1]">
            SatQuery AI — System Architecture
          </h2>
          <p className="font-['Inter'] text-sm text-[#b9cacb] mt-2 max-w-3xl leading-relaxed">
            An Interactive Vision-Language Assistant for Multimodal Remote Sensing Image Analysis through Text Queries.
            Engineered with an evidence-driven, agentic orchestrator that dynamically selects specialist models,
            combines optical and SAR observations, and explains findings with an auditable trace.
          </p>
        </header>

        {/* Core Pillars Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="glass-panel rounded-xl p-5 bg-[#171b26]/70 border border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <span className="w-9 h-9 rounded-lg bg-[#00f2ff]/15 text-[#00f2ff] flex items-center justify-center">
                <span className="material-symbols-outlined text-[20px]">psychology</span>
              </span>
              <h3 className="font-['Geist',sans-serif] text-base font-bold text-[#dfe2f1]">
                Agentic Orchestration & Planning
              </h3>
            </div>
            <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
              Converts unstructured natural language into structured evidence plans. Rather than relying on black-box VLM hallucinations, SatQuery determines which observations are needed, executes specialist tools, and validates evidence sufficiency.
            </p>
          </div>

          <div className="glass-panel rounded-xl p-5 bg-[#171b26]/70 border border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <span className="w-9 h-9 rounded-lg bg-[#74f5ff]/15 text-[#74f5ff] flex items-center justify-center">
                <span className="material-symbols-outlined text-[20px]">layers</span>
              </span>
              <h3 className="font-['Geist',sans-serif] text-base font-bold text-[#dfe2f1]">
                Optical + SAR Multimodal Fusion
              </h3>
            </div>
            <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
              Harmonizes multispectral optical reflection (NDVI, NDWI) with SAR radar backscatter (C-Band VV/VH, Lee speckle filtering). This enables reliable insights even during persistent cloud cover or heavy atmospheric haze.
            </p>
          </div>

          <div className="glass-panel rounded-xl p-5 bg-[#171b26]/70 border border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <span className="w-9 h-9 rounded-lg bg-[#adc6ff]/15 text-[#adc6ff] flex items-center justify-center">
                <span className="material-symbols-outlined text-[20px]">compare</span>
              </span>
              <h3 className="font-['Geist',sans-serif] text-base font-bold text-[#dfe2f1]">
                Bi-Temporal Change Understanding
              </h3>
            </div>
            <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
              Provides robust sub-pixel image coregistration (ORB/ECC), normalized feature differencing, change mask segmentation, and spatial area footprint quantification across multi-year temporal baselines.
            </p>
          </div>

          <div className="glass-panel rounded-xl p-5 bg-[#171b26]/70 border border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <span className="w-9 h-9 rounded-lg bg-[#00dbe7]/15 text-[#00dbe7] flex items-center justify-center">
                <span className="material-symbols-outlined text-[20px]">verified</span>
              </span>
              <h3 className="font-['Geist',sans-serif] text-base font-bold text-[#dfe2f1]">
                CPU-First & Calibrated Confidence
              </h3>
            </div>
            <p className="font-['Inter'] text-xs text-[#b9cacb] leading-relaxed">
              Built to operate on standard consumer laptops with zero mandatory GPU dependencies. Generates auditable step-by-step traces and calibrated numerical confidence based on inter-sensor agreement.
            </p>
          </div>
        </div>

        {/* Prescribed Benchmarks & Datasets */}
        <div className="glass-panel rounded-xl p-6 bg-[#171b26]/80 border border-white/10">
          <h3 className="font-['Geist',sans-serif] text-base font-bold text-[#dfe2f1] mb-4 flex items-center gap-2">
            <span className="material-symbols-outlined text-[#00f2ff]">dataset</span>
            <span>Mandatory Benchmarks & Training Datasets</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 rounded-lg bg-[#0a0e18] border border-white/5 space-y-1.5">
              <div className="font-['JetBrains_Mono'] text-xs font-bold text-[#00f2ff]">BigEarthNet.txt</div>
              <div className="text-[11px] font-['Inter'] text-[#dfe2f1] font-medium">Primary Adaptation</div>
              <div className="text-[10px] font-['Inter'] text-[#849495]">Multi-spectral Sentinel-2 & Sentinel-1 land cover patches for adapter training.</div>
            </div>

            <div className="p-4 rounded-lg bg-[#0a0e18] border border-white/5 space-y-1.5">
              <div className="font-['JetBrains_Mono'] text-xs font-bold text-[#74f5ff]">VRSBench</div>
              <div className="text-[11px] font-['Inter'] text-[#dfe2f1] font-medium">Captioning & Grounding</div>
              <div className="text-[10px] font-['Inter'] text-[#849495]">High-res RS visual question answering, scene description, and bounding box grounding.</div>
            </div>

            <div className="p-4 rounded-lg bg-[#0a0e18] border border-white/5 space-y-1.5">
              <div className="font-['JetBrains_Mono'] text-xs font-bold text-[#adc6ff]">RSVQA</div>
              <div className="text-[11px] font-['Inter'] text-[#dfe2f1] font-medium">Single-Image VQA</div>
              <div className="text-[10px] font-['Inter'] text-[#849495]">Quantitative and qualitative query answering over Sentinel-2 and High-Res RGB imagery.</div>
            </div>

            <div className="p-4 rounded-lg bg-[#0a0e18] border border-white/5 space-y-1.5">
              <div className="font-['JetBrains_Mono'] text-xs font-bold text-[#00dbe7]">CDVQA</div>
              <div className="text-[11px] font-['Inter'] text-[#dfe2f1] font-medium">Change-Based VQA</div>
              <div className="text-[10px] font-['Inter'] text-[#849495]">Bi-temporal change evaluation for structural, environmental, and disaster scenarios.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
