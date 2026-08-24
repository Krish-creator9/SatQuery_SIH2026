import React, { useState } from 'react';

/**
 * SatQuery AI — Query History Component (Exact Stitch Screen Mapping)
 */
export default function QueryHistory({ history = [], onReplayQuery, onClearHistory }) {
  const [search, setSearch] = useState('');
  const [selectedScenario, setSelectedScenario] = useState('All');

  const defaultRecords = [
    {
      id: 'EX-8924A',
      query: 'Identify new structures built between the two dates and estimate their area.',
      scenario: 'Urban Expansion',
      tag: 'Strategic',
      tagColor: 'error',
      timestamp: '2026-08-24T14:05:12Z',
      confidence: 94,
      mode: 'change',
    },
    {
      id: 'EX-8923B',
      query: 'Where are the flood-affected regions and how much did water extent increase?',
      scenario: 'Disaster Response',
      tag: 'Infrastructure',
      tagColor: 'secondary',
      timestamp: '2026-08-24T13:42:09Z',
      confidence: 88,
      mode: 'fusion',
    },
    {
      id: 'EX-8919C',
      query: 'Which regions show vegetation stress and where has crop health decreased?',
      scenario: 'Agriculture Monitoring',
      tag: 'Tactical',
      tagColor: 'primary',
      timestamp: '2026-08-24T12:18:55Z',
      confidence: 72,
      mode: 'single',
    },
  ];

  const records = history.length > 0
    ? history.map((h, i) => ({
        id: h.id || `EX-89${25 + i}A`,
        query: h.query,
        scenario: h.mode === 'fusion' ? 'Disaster Response' : h.mode === 'single' ? 'Agriculture Monitoring' : 'Urban Expansion',
        tag: h.mode === 'fusion' ? 'Infrastructure' : h.mode === 'single' ? 'Tactical' : 'Strategic',
        tagColor: h.mode === 'fusion' ? 'secondary' : h.mode === 'single' ? 'primary' : 'error',
        timestamp: h.timestamp || new Date().toISOString(),
        confidence: h.confidence ? Math.round(h.confidence * 100) : 87,
        mode: h.mode || 'change',
      }))
    : defaultRecords;

  const filteredRecords = records.filter((rec) => {
    const matchesSearch =
      rec.query.toLowerCase().includes(search.toLowerCase()) ||
      rec.id.toLowerCase().includes(search.toLowerCase()) ||
      rec.scenario.toLowerCase().includes(search.toLowerCase());
    const matchesScenario =
      selectedScenario === 'All' || rec.tag.toLowerCase() === selectedScenario.toLowerCase();
    return matchesSearch && matchesScenario;
  });

  const exportCSV = () => {
    const csvContent =
      'data:text/csv;charset=utf-8,' +
      ['Execution ID,Query,Scenario Tag,Timestamp,Confidence']
        .concat(
          filteredRecords.map(
            (r) => `"${r.id}","${r.query.replace(/"/g, '""')}","${r.tag}","${r.timestamp}","${r.confidence}%"`
          )
        )
        .join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'satquery_execution_history.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex-1 w-full min-h-screen flex flex-col relative z-0 bg-[#0f131d] overflow-y-auto">
      {/* Page Header & Filter Bar */}
      <header className="sticky top-0 z-10 bg-[#0f131d]/90 backdrop-blur-xl border-b border-white/10 px-8 py-6 flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-['Geist',sans-serif] text-2xl md:text-3xl font-bold text-[#00dbe7]">
              Query Execution History
            </h2>
            <p className="text-sm text-[#b9cacb] mt-1 font-['Inter']">
              Past operational queries, telemetry, and intelligence records.
            </p>
          </div>
          <button
            onClick={exportCSV}
            className="bg-[#262a35] border border-[#3a494b] hover:border-[#00f2ff] text-[#00dbe7] px-4 py-2 rounded-lg flex items-center gap-2 transition-all shadow-[0_0_0_rgba(0,242,255,0)] hover:shadow-[0_0_15px_rgba(0,242,255,0.2)] cursor-pointer text-xs font-['JetBrains_Mono'] font-semibold"
          >
            <span className="material-symbols-outlined text-[16px]">download</span>
            <span>Export CSV</span>
          </button>
        </div>

        {/* Search and Filter Controls */}
        <div className="flex flex-wrap gap-4 items-center bg-[#171b26]/50 p-2.5 rounded-lg border border-white/5">
          <div className="relative flex-1 min-w-[280px]">
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-[#849495] text-[18px]">
              search
            </span>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-[#0a0e18] border border-[#3a494b] rounded-md py-2 pl-9 pr-3 text-[#dfe2f1] font-['JetBrains_Mono'] text-xs focus:ring-1 focus:ring-[#00f2ff] focus:border-[#00f2ff] transition-colors placeholder:text-[#849495]/60 outline-none"
              placeholder="Search query text, tags, or execution ID..."
              type="text"
            />
          </div>

          <div className="flex gap-2">
            <select
              value={selectedScenario}
              onChange={(e) => setSelectedScenario(e.target.value)}
              className="bg-[#0a0e18] border border-[#3a494b] rounded-md py-2 px-3 text-[#dfe2f1] font-['JetBrains_Mono'] text-xs focus:ring-1 focus:ring-[#00f2ff] focus:border-[#00f2ff] outline-none cursor-pointer"
            >
              <option value="All">All Scenarios</option>
              <option value="Strategic">Strategic</option>
              <option value="Tactical">Tactical</option>
              <option value="Infrastructure">Infrastructure</option>
            </select>
          </div>
        </div>
      </header>

      {/* Data Canvas */}
      <div className="p-8 flex-1 overflow-x-auto">
        {/* Glass Card Table Container */}
        <div className="bg-[#1c1f2a]/60 backdrop-blur-md border border-white/10 rounded-xl overflow-hidden shadow-xl">
          <table className="w-full text-left border-collapse whitespace-nowrap">
            <thead>
              <tr className="border-b border-white/10 bg-[#262a35]/40 font-['JetBrains_Mono'] text-[11px] text-[#b9cacb] uppercase tracking-wider">
                <th className="py-3 px-6">Execution ID</th>
                <th className="py-3 px-6">Query Intent</th>
                <th className="py-3 px-6">Scenario Tag</th>
                <th className="py-3 px-6">Timestamp (UTC)</th>
                <th className="py-3 px-6">Confidence</th>
                <th className="py-3 px-6 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 font-['JetBrains_Mono'] text-xs">
              {filteredRecords.map((item) => (
                <tr key={item.id} className="group hover:bg-[#313540]/30 transition-colors">
                  <td className="py-3.5 px-6 text-[#adc6ff] font-bold">{item.id}</td>
                  <td
                    className="py-3.5 px-6 text-[#dfe2f1] font-['Inter'] text-sm max-w-[320px] truncate"
                    title={item.query}
                  >
                    {item.query}
                  </td>
                  <td className="py-3.5 px-6">
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] uppercase font-bold tracking-wider ${
                        item.tagColor === 'error'
                          ? 'bg-[#93000a]/20 border border-[#ffb4ab]/30 text-[#ffb4ab]'
                          : item.tagColor === 'secondary'
                          ? 'bg-[#0566d9]/20 border border-[#adc6ff]/30 text-[#adc6ff]'
                          : 'bg-[#006a71]/20 border border-[#00f2ff]/30 text-[#00dbe7]'
                      }`}
                    >
                      {item.tag}
                    </span>
                  </td>
                  <td className="py-3.5 px-6 text-[#849495]">{item.timestamp}</td>
                  <td className="py-3.5 px-6">
                    <div className="flex items-center gap-2">
                      <span className="text-[#00f2ff] font-bold">{item.confidence}%</span>
                      <div className="h-1.5 w-16 bg-[#313540] rounded-full overflow-hidden">
                        <div
                          className="h-full bg-[#00f2ff] shadow-[0_0_8px_rgba(0,242,255,0.6)]"
                          style={{ width: `${item.confidence}%` }}
                        />
                      </div>
                    </div>
                  </td>
                  <td className="py-3.5 px-6 text-right">
                    <button
                      onClick={() => onReplayQuery && onReplayQuery(item)}
                      className="text-[#74f5ff] hover:text-[#00f2ff] transition-colors inline-flex items-center gap-1 font-['JetBrains_Mono'] text-xs font-semibold cursor-pointer"
                    >
                      Replay <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Pagination Footer */}
          <div className="border-t border-white/10 p-4 flex items-center justify-between bg-[#0a0e18]/50 font-['JetBrains_Mono'] text-xs text-[#b9cacb]">
            <span>Showing 1-{filteredRecords.length} of {filteredRecords.length} records</span>
            <div className="flex gap-2">
              <span className="text-[#00f2ff]">Page 1 of 1</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
