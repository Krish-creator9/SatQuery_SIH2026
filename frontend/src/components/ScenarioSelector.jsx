import React from 'react';

/**
 * SatQuery AI — Scenario Selector Component (Stitch Design)
 */
export default function ScenarioSelector({ onSelectScenario }) {
  const scenarios = [
    {
      id: 'disaster',
      title: 'Disaster Response',
      icon: 'water_damage',
      accentColor: '#00f2ff',
      bgImage: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCuF3_Zssdungnk3yUE_0L9AhPnZFuJ_jo7XEd-61DuXNvuOYa52CNz5L7CMPp4_bpXX_dIrXI0xKXlMr77TAWS4YzxIBb0ezPM0Vf426C84C6kKlTj1uvudQGnIZhHI2AgG3NEIb-3wNR0K7VBMAldd_UW7TEqhziEoj_ag_2O62Qx7SBzDDQBZaq3XWCUxhy4jXb82RVV_vx7WSd0x5Q6MGunubYlQ0wleY9NNHtKGnVJsowfIOuK',
      description: 'Rapid assessment of flood extents, infrastructure damage, and optimal resource allocation routing using Optical + SAR radar passes.',
      queries: ['Show flooded roads', 'Assess building damage', 'Find safe zones', 'SAR flood extent delta'],
      defaultQuery: 'Where are the flood-affected regions and how much did water extent increase?',
      mode: 'fusion',
    },
    {
      id: 'agriculture',
      title: 'Agriculture Monitoring',
      icon: 'eco',
      accentColor: '#74f5ff',
      bgImage: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD85e7knO2UVkLhaZDcFt_tZgOSaSkuRp7Cal9bwYZbBZLx8UMPu2vJf5uUR9QtmCIdQk__k95vis5yFQN0FseOCxH6LIQsD_UACbbtBJO7DeQ_A0di0vgep1Qwup_FsJQPC0F1EqfoMuWP6aj8vxJzHkPKrHuvQ11km2KW4cMjYE_dOEF9kxKqQWb2TCKYizKIPTCyrwISInnAVd-0m3aHwoRpt8Lqu_UukNJYbEt9iSzdf3_R4pok',
      description: 'Track crop health, predict yield variations, and monitor irrigation levels across vast regions using NDVI and NDWI spectral indices.',
      queries: ['NDVI anomalies', 'Water stress areas', 'Crop classification', 'Crop condition delta'],
      defaultQuery: 'Which regions show vegetation stress and where has crop health decreased between the two dates?',
      mode: 'change',
    },
    {
      id: 'urban',
      title: 'Urban Expansion',
      icon: 'location_city',
      accentColor: '#adc6ff',
      bgImage: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDnln1IqIZwO-46I_uGOgqt4bSI_lVkvfnmL3Xd8bawKq4CTykjy-XS4QublnP3xymLc-0YIfLWG2IfZ29u1nxPFdiTu4RNN-8IYYt_DGMBekThcJ6m2TOMcruaJWDRBchvvi7t9bYcwfRYjEnd5IZBQhsI1DObehMpH3q-t0ffrpszlFxy46Nmt40QLveJ0oKKgdtx4gNbO7iw_nmAnLcbX9kJbBN-j7jopIIT1CDrgUtjUEm_hTlI',
      description: 'Analyze sprawl, detect informal settlements, and track structural changes over multi-year periods with bi-temporal change detection.',
      queries: ['New construction 2023', 'Deforestation vs Urban', 'Road network growth', 'Industrial expansion'],
      defaultQuery: 'Identify new structures built between the two dates and estimate their area and expansion percentage.',
      mode: 'change',
    },
  ];

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#1c1f2a]/60 via-[#0f131d] to-[#0a0e18]">
      <div className="max-w-5xl mx-auto w-full mb-8">
        <div className="font-['JetBrains_Mono'] text-xs text-[#00f2ff] uppercase tracking-widest mb-2">
          Operational Scenarios
        </div>
        <h2 className="font-['Geist',sans-serif] text-3xl font-bold text-[#dfe2f1] mb-2">
          Select Mission Scenario
        </h2>
        <p className="font-['Inter'] text-sm text-[#b9cacb] max-w-2xl leading-relaxed">
          Choose a primary operational context. This selection pre-configures the AI agent's baseline models,
          relevant satellite data sources, and analytical tools for your session.
        </p>
      </div>

      {/* Bento Grid */}
      <div className="max-w-5xl mx-auto w-full grid grid-cols-1 lg:grid-cols-3 gap-6 pb-12">
        {scenarios.map((scenario) => (
          <div
            key={scenario.id}
            onClick={() => onSelectScenario(scenario)}
            className="group relative rounded-xl overflow-hidden bg-[#171b26] border border-white/10 flex flex-col glow-hover transition-all duration-300 hover:-translate-y-1.5 cursor-pointer shadow-xl min-h-[420px]"
          >
            {/* Background Image Layer */}
            <div className="absolute inset-0 z-0 overflow-hidden">
              <div
                className="w-full h-full bg-cover bg-center opacity-30 group-hover:opacity-50 transition-opacity duration-500 blur-[1px] group-hover:blur-0 scale-100 group-hover:scale-105 transition-transform duration-700"
                style={{ backgroundImage: `url('${scenario.bgImage}')` }}
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#0a0e18] via-[#171b26]/85 to-transparent" />
            </div>

            {/* Card Content Layer */}
            <div className="relative z-10 p-6 flex flex-col h-full">
              {/* Icon */}
              <div className="w-12 h-12 rounded-lg bg-[#262a35]/80 border border-white/10 flex items-center justify-center mb-4 group-hover:border-[#00f2ff] transition-colors backdrop-blur-md">
                <span
                  className="material-symbols-outlined text-[28px] text-[#b9cacb] group-hover:text-[#00f2ff] transition-colors fill"
                >
                  {scenario.icon}
                </span>
              </div>

              {/* Title & Description */}
              <h3 className="font-['Geist',sans-serif] text-xl font-bold text-[#dfe2f1] mb-2 group-hover:text-[#00f2ff] transition-colors">
                {scenario.title}
              </h3>
              <p className="font-['Inter'] text-xs text-[#b9cacb] mb-6 flex-1 leading-relaxed">
                {scenario.description}
              </p>

              {/* Suggested Queries */}
              <div className="space-y-2 mt-auto">
                <div className="text-[10px] uppercase tracking-widest text-[#849495] font-['JetBrains_Mono']">
                  Suggested Queries
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {scenario.queries.map((q, idx) => (
                    <span
                      key={idx}
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectScenario({ ...scenario, defaultQuery: q });
                      }}
                      className="bg-[#313540]/60 hover:bg-[#00f2ff]/20 border border-white/10 hover:border-[#00f2ff]/50 text-[#dfe2f1] hover:text-[#00f2ff] rounded-full px-2.5 py-1 font-['JetBrains_Mono'] text-[10px] backdrop-blur-sm transition-colors cursor-pointer"
                    >
                      {q}
                    </span>
                  ))}
                </div>
              </div>

              {/* Launch CTA */}
              <div className="mt-5 pt-3 border-t border-white/10 flex items-center justify-between text-xs font-['JetBrains_Mono'] text-[#00f2ff]">
                <span>INITIALIZE SCENARIO</span>
                <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">
                  arrow_forward
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
