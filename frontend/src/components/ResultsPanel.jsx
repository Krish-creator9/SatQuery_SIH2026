/**
 * ResultsPanel — Displays the fused analysis result.
 * Shows answer, confidence, evidence, and execution trace.
 */
export default function ResultsPanel({ result }) {
  if (!result) {
    return (
      <div className="card">
        <div className="empty-state">
          <div className="empty-state-icon">🌍</div>
          <div className="empty-state-title">Ready to Analyze</div>
          <div className="empty-state-text">
            Upload remote sensing imagery and ask a question.
            SatQuery will determine what evidence is needed,
            run the appropriate analyses, and present grounded results.
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="right-panel">
      {/* Answer */}
      <div className="card">
        <div className="card-title">
          <span className="card-title-icon">📋</span>
          Answer
        </div>
        <div className="result-answer">{result.answer}</div>
      </div>

      {/* Confidence */}
      <div className="card">
        <div className="card-title">
          <span className="card-title-icon">📊</span>
          Confidence
        </div>
        <ConfidenceGauge value={result.confidence} />
      </div>

      {/* Evidence */}
      {result.evidence_summary && result.evidence_summary.length > 0 && (
        <div className="card">
          <div className="card-title">
            <span className="card-title-icon">🔍</span>
            Evidence
          </div>
          <EvidenceCards evidence={result.evidence_summary} />
        </div>
      )}

      {/* Warnings */}
      {result.warnings && result.warnings.length > 0 && (
        <div className="card">
          {result.warnings.map((w, i) => (
            <div key={i} className="warning-banner" style={{ marginBottom: i < result.warnings.length - 1 ? '8px' : 0 }}>
              ⚠️ {w}
            </div>
          ))}
        </div>
      )}

      {/* Insufficient Data Notice */}
      {result.insufficient_data && (
        <div className="card">
          <div className="insufficient-data-banner">
            ℹ️ {result.insufficient_data}
          </div>
        </div>
      )}

      {/* Execution Trace */}
      {result.execution_trace && result.execution_trace.length > 0 && (
        <div className="card">
          <div className="card-title">
            <span className="card-title-icon">⚡</span>
            Execution Trace
          </div>
          <ExecutionTrace steps={result.execution_trace} />
        </div>
      )}
    </div>
  );
}

/* === Sub-components === */

function ConfidenceGauge({ value }) {
  const pct = Math.round(value * 100);
  const circumference = 2 * Math.PI * 26;
  const offset = circumference - (value * circumference);
  const color = value >= 0.7 ? 'var(--color-confidence-high)'
    : value >= 0.4 ? 'var(--color-confidence-medium)'
    : 'var(--color-confidence-low)';

  return (
    <div className="confidence-container">
      <div className="confidence-ring">
        <svg width="64" height="64" viewBox="0 0 64 64">
          <circle className="confidence-ring-bg" cx="32" cy="32" r="26" />
          <circle
            className="confidence-ring-fill"
            cx="32" cy="32" r="26"
            stroke={color}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
          />
        </svg>
        <div className="confidence-value" style={{ color }}>{pct}%</div>
      </div>
      <div className="confidence-label">
        {value === 0
          ? 'No analysis performed'
          : value >= 0.7
          ? 'High confidence — strong evidence agreement'
          : value >= 0.4
          ? 'Moderate confidence — partial evidence'
          : 'Low confidence — limited or conflicting evidence'}
      </div>
    </div>
  );
}

function EvidenceCards({ evidence }) {
  return (
    <div className="evidence-grid">
      {evidence.map((e, i) => (
        <div key={i} className="evidence-card">
          <div className={`evidence-source ${e.source || ''}`}>
            {e.source || 'Unknown'}
          </div>
          <span className={`evidence-verdict ${e.verdict || 'neutral'}`}>
            {e.verdict || 'pending'}
          </span>
          {e.detail && <div className="evidence-detail">{e.detail}</div>}
        </div>
      ))}
    </div>
  );
}

function ExecutionTrace({ steps }) {
  return (
    <div className="execution-trace">
      {steps.map((step) => (
        <div key={step.step_number} className="trace-step">
          <div className="trace-step-number">{step.step_number}</div>
          <div className="trace-step-content">
            <span className="trace-step-module">{step.module}</span>
            {' → '}
            <span className="trace-step-action">{step.action}</span>
            {step.duration_ms > 0 && (
              <span className="trace-step-time"> ({step.duration_ms}ms)</span>
            )}
            {step.detail && (
              <div style={{ color: 'var(--color-text-muted)', marginTop: '2px' }}>
                {step.detail}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
