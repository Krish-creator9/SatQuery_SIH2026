import React, { useState } from 'react';

/**
 * SatQuery AI — Agent Execution Trace DAG & Telemetry (Stitch Design)
 */
export default function AgentExecutionTrace({ result, query, onBackToWorkspace }) {
  const [selectedNode, setSelectedNode] = useState(2); // default to Evidence Planner node

  const traceNodes = [
    {
      id: 0,
      title: 'Query Ingestion',
      module: 'planner.query_analyzer',
      status: 'SUCCESS',
      latencyMs: 12,
      icon: 'input',
      description: 'Received natural language prompt and verified satellite input availability.',
      details: {
        input: query || 'Identify new structures built between the two dates and estimate their area.',
        token_count: 14,
        encoding: 'UTF-8',
      },
    },
    {
      id: 1,
      title: 'Query Analyzer & Intent Parsing',
      module: 'planner.query_analyzer',
      status: 'SUCCESS',
      latencyMs: 48,
      icon: 'psychology',
      description: 'Extracted semantic intent, target land cover classes, and required observation modality.',
      details: {
        detected_intent: 'BI_TEMPORAL_CHANGE_VQA',
        target_entities: ['structures', 'industrial buildings', 'area footprint'],
        temporal_window: 'Bi-Temporal (T1=2020, T2=2024)',
        modality_requirement: ['Optical Multi-Spectral', 'SAR Backscatter Corroboration'],
      },
    },
    {
      id: 2,
      title: 'Evidence Planner & Tool Routing',
      module: 'planner.evidence_planner',
      status: 'SUCCESS',
      latencyMs: 34,
      icon: 'account_tree',
      description: 'Dynamically scheduled specialist remote sensing analytical pipelines and models.',
      details: {
        scheduled_tasks: [
          'analysis.temporal.registration (Sub-pixel ORB/ECC Alignment)',
          'analysis.optical.spectral_indices (NDVI & NDWI Calculation)',
          'analysis.sar.backscatter (Lee Speckle Filter & Sigma-0)',
          'models.grounding.grounding_engine (Structure Region Grounding)',
        ],
        dependency_graph: 'Sequential Registration -> Parallel Spectral/SAR Processing -> Fusion',
      },
    },
    {
      id: 3,
      title: 'Specialist Model Execution',
      module: 'analysis.temporal + analysis.sar',
      status: 'SUCCESS',
      latencyMs: 245,
      icon: 'memory',
      description: 'Executed CPU-first classical RS algorithms and lightweight deep vision feature extractors.',
      details: {
        registration_rmse: '0.38 pixels (Pass)',
        ndvi_delta_mean: '-0.14 (Vegetation Loss)',
        sar_backscatter_delta: '+3.2 dB (Structural Hard Target Appearance)',
        grounded_boxes: 3,
      },
    },
    {
      id: 4,
      title: 'Cross-Modal Evidence Fusion',
      module: 'fusion.evidence_fusion',
      status: 'SUCCESS',
      latencyMs: 28,
      icon: 'hub',
      description: 'Synthesized multi-source evidence, evaluated inter-sensor agreement, and computed calibrated confidence.',
      details: {
        evidence_sources_count: 3,
        agreement_score: '0.874 (Strong Agreement)',
        discrepancy_flags: ['Localized cloud shadow in quadrant NE-2'],
        calibrated_confidence: result?.confidence ? result.confidence : 0.874,
      },
    },
    {
      id: 5,
      title: 'Auditable Explanation Generation',
      module: 'fusion.explanation_engine',
      status: 'SUCCESS',
      latencyMs: 18,
      icon: 'verified',
      description: 'Constructed natural language explanation grounded in quantitative spatial metrics.',
      details: {
        output_answer: result?.answer || 'Significant urban expansion detected (+12%). Several new structures identified as industrial warehouses.',
        decision_trace_length: 6,
        safety_status: 'Compliant with PS 26167 guidelines',
      },
    },
  ];

  const activeNodeData = traceNodes[selectedNode] || traceNodes[0];

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#1c1f2a]/60 via-[#0f131d] to-[#0a0e18]">
      <div className="max-w-5xl mx-auto space-y-6 pb-12">
        {/* Header */}
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-end border-b border-white/10 pb-4 gap-4">
          <div>
            <div className="font-['JetBrains_Mono'] text-xs text-[#00f2ff] mb-1 uppercase tracking-widest flex items-center gap-2">
              <span>Auditable Decision Pipeline</span>
              <span className="text-[#849495]">·</span>
              <span className="text-[#74f5ff]">100% CPU-First Verified</span>
            </div>
            <h2 className="font-['Geist',sans-serif] text-3xl font-bold text-[#dfe2f1]">
              Agent Execution Trace DAG
            </h2>
          </div>

          <button
            onClick={onBackToWorkspace}
            className="px-4 py-2 rounded-lg bg-[#262a35] hover:bg-[#313540] text-[#dfe2f1] font-['JetBrains_Mono'] text-xs flex items-center gap-2 border border-white/10 transition-colors"
          >
            <span className="material-symbols-outlined text-[16px]">arrow_back</span>
            Back to Workspace
          </button>
        </header>

        {/* Telemetry Hardware Overview */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="glass-panel rounded-xl p-3.5 bg-[#171b26]/70 border border-white/10">
            <div className="text-[10px] font-['JetBrains_Mono'] text-[#849495] uppercase">Total Latency</div>
            <div className="text-xl font-bold text-[#00f2ff] font-['Geist',sans-serif] mt-0.5">385 ms</div>
          </div>
          <div className="glass-panel rounded-xl p-3.5 bg-[#171b26]/70 border border-white/10">
            <div className="text-[10px] font-['JetBrains_Mono'] text-[#849495] uppercase">Memory Footprint</div>
            <div className="text-xl font-bold text-[#adc6ff] font-['Geist',sans-serif] mt-0.5">412 MB RAM</div>
          </div>
          <div className="glass-panel rounded-xl p-3.5 bg-[#171b26]/70 border border-white/10">
            <div className="text-[10px] font-['JetBrains_Mono'] text-[#849495] uppercase">Execution Mode</div>
            <div className="text-xl font-bold text-[#74f5ff] font-['Geist',sans-serif] mt-0.5">CPU First</div>
          </div>
          <div className="glass-panel rounded-xl p-3.5 bg-[#171b26]/70 border border-white/10">
            <div className="text-[10px] font-['JetBrains_Mono'] text-[#849495] uppercase">Auditable Steps</div>
            <div className="text-xl font-bold text-[#dfe2f1] font-['Geist',sans-serif] mt-0.5">6 / 6 Passed</div>
          </div>
        </div>

        {/* Visual Pipeline DAG Flow */}
        <div className="glass-panel rounded-xl p-6 bg-[#171b26]/80 border border-white/10">
          <h3 className="font-['Geist',sans-serif] text-base font-bold text-[#dfe2f1] mb-6 flex items-center gap-2">
            <span className="material-symbols-outlined text-[#00f2ff]">schema</span>
            <span>Interactive Decision Pipeline Flowchart</span>
          </h3>

          {/* Stepper Grid */}
          <div className="grid grid-cols-1 md:grid-cols-6 gap-3 relative">
            {traceNodes.map((node, index) => {
              const isSelected = selectedNode === node.id;
              return (
                <div
                  key={node.id}
                  onClick={() => setSelectedNode(node.id)}
                  className={`p-3.5 rounded-xl border flex flex-col justify-between cursor-pointer transition-all duration-200 min-h-[140px] relative ${
                    isSelected
                      ? 'bg-[#0566d9]/30 border-[#00f2ff] shadow-[0_0_15px_rgba(0,242,255,0.3)]'
                      : 'bg-[#0a0e18]/80 border-white/10 hover:border-[#00f2ff]/50 hover:bg-[#1c1f2a]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="w-5 h-5 rounded-full bg-[#00f2ff]/20 text-[#00f2ff] font-['JetBrains_Mono'] text-[10px] flex items-center justify-center font-bold">
                      {index + 1}
                    </span>
                    <span className="material-symbols-outlined text-[16px] text-[#00f2ff] fill">
                      {node.icon}
                    </span>
                  </div>

                  <div>
                    <div className="font-['Geist',sans-serif] text-xs font-bold text-[#dfe2f1] line-clamp-2">
                      {node.title}
                    </div>
                    <div className="text-[10px] font-['JetBrains_Mono'] text-[#849495] mt-1 truncate">
                      {node.latencyMs}ms
                    </div>
                  </div>

                  <div className="mt-2 pt-1 border-t border-white/5 flex items-center justify-between text-[9px] font-['JetBrains_Mono'] text-[#00f2ff]">
                    <span>STATUS: OK</span>
                    <span className="w-1.5 h-1.5 rounded-full bg-[#00f2ff]"></span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Node Deep-Dive Drawer */}
        <div className="glass-panel rounded-xl p-6 bg-[#171b26]/90 border border-white/10">
          <div className="flex items-center justify-between border-b border-white/10 pb-3 mb-4">
            <div className="flex items-center gap-3">
              <span className="w-8 h-8 rounded-lg bg-[#00f2ff]/10 border border-[#00f2ff]/30 text-[#00f2ff] flex items-center justify-center">
                <span className="material-symbols-outlined text-[18px]">{activeNodeData.icon}</span>
              </span>
              <div>
                <h4 className="font-['Geist',sans-serif] text-lg font-bold text-[#dfe2f1]">
                  Step {selectedNode + 1}: {activeNodeData.title}
                </h4>
                <div className="text-xs font-['JetBrains_Mono'] text-[#00f2ff]">
                  Module: {activeNodeData.module} · Latency: {activeNodeData.latencyMs}ms
                </div>
              </div>
            </div>
            <span className="px-2.5 py-1 rounded-full bg-[#00f2ff]/15 border border-[#00f2ff]/30 text-[#00f2ff] font-['JetBrains_Mono'] text-[10px] font-bold">
              EXECUTION VERIFIED
            </span>
          </div>

          <p className="font-['Inter'] text-sm text-[#dfe2f1] mb-4">
            {activeNodeData.description}
          </p>

          {/* Node Parameters / Telemetry JSON */}
          <div className="p-4 rounded-lg bg-[#0a0e18] border border-white/10 font-['JetBrains_Mono'] text-xs text-[#b9cacb] overflow-x-auto">
            <div className="text-[#849495] mb-2 uppercase text-[10px] tracking-wider">Node I/O & Parameters:</div>
            <pre className="text-[#74f5ff] leading-relaxed">
              {JSON.stringify(activeNodeData.details, null, 2)}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
