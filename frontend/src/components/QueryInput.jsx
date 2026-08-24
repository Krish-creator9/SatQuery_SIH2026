import { useState } from 'react';

const SUGGESTIONS = [
  "Has vegetation increased?",
  "Show water bodies",
  "Compare before and after",
  "What changed between dates?",
  "Analyze SAR and optical",
  "Where are built-up areas?",
];

/**
 * QueryInput — Natural language query input with suggestions.
 */
export default function QueryInput({ onSubmit, loading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = () => {
    if (query.trim() && !loading) {
      onSubmit(query.trim());
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="card">
      <div className="card-title">
        <span className="card-title-icon">💬</span>
        Query
      </div>

      <div className="query-input-container">
        <textarea
          id="query-input"
          className="query-input"
          placeholder="Ask about your satellite imagery..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button
          className="query-submit-btn"
          onClick={handleSubmit}
          disabled={!query.trim() || loading}
          title="Analyze"
          id="query-submit-btn"
        >
          {loading ? '⏳' : '→'}
        </button>
      </div>

      <div className="query-suggestions">
        {SUGGESTIONS.map((suggestion) => (
          <button
            key={suggestion}
            className="query-suggestion"
            onClick={() => {
              setQuery(suggestion);
            }}
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  );
}
