import { useState, useEffect } from 'react';
import ImageUploader from './components/ImageUploader.jsx';
import QueryInput from './components/QueryInput.jsx';
import ResultsPanel from './components/ResultsPanel.jsx';
import { uploadImage, sendQuery, getHealth } from './services/api.js';

/**
 * SatQuery AI — Main Application
 *
 * Dashboard layout:
 * - Header: logo, status
 * - Left panel: upload + query
 * - Right panel: results (answer, confidence, evidence, trace)
 */
export default function App() {
  const [sessionId, setSessionId] = useState(null);
  const [images, setImages] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking');
  const [error, setError] = useState(null);

  // Check backend health on mount
  useEffect(() => {
    getHealth()
      .then(() => setBackendStatus('healthy'))
      .catch(() => setBackendStatus('offline'));
  }, []);

  // Handle image upload
  const handleUpload = async (file) => {
    try {
      const response = await uploadImage(file, 'unknown', 'primary', sessionId);
      setSessionId(response.session_id);
      setImages((prev) => [...prev, {
        id: response.image_id,
        filename: response.filename,
        metadata: response.metadata,
        preview: response.preview_path,
        sizeMb: response.file_size_mb,
      }]);
      setError(null);
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  // Handle query submission
  const handleQuery = async (query) => {
    setLoading(true);
    setError(null);
    try {
      const response = await sendQuery(query, sessionId);
      setResult(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="app-logo">
          <div className="app-logo-icon">SQ</div>
          <div>
            <h1>SatQuery AI</h1>
            <div className="app-logo-subtitle">
              Remote Sensing Analysis · SIH 2026
            </div>
          </div>
        </div>
        <div className="header-status">
          <div className="status-badge">
            <div className={`status-dot ${backendStatus !== 'healthy' ? '' : ''}`}
              style={{
                background: backendStatus === 'healthy'
                  ? 'var(--color-success)'
                  : backendStatus === 'checking'
                  ? 'var(--color-warning)'
                  : 'var(--color-error)',
              }}
            />
            {backendStatus === 'healthy' ? 'Backend Connected' :
             backendStatus === 'checking' ? 'Connecting...' :
             'Backend Offline'}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="main-content">
        {/* Left Panel */}
        <div className="left-panel">
          <ImageUploader onUpload={handleUpload} sessionId={sessionId} />

          {/* Uploaded Images List */}
          {images.length > 0 && (
            <div className="card">
              <div className="card-title">
                <span className="card-title-icon">🖼️</span>
                Uploaded ({images.length})
              </div>
              <div className="uploaded-images">
                {images.map((img) => (
                  <div key={img.id} className="image-preview-card">
                    <div className="image-preview-thumb"
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'var(--color-text-muted)',
                        fontSize: '1.5rem',
                      }}
                    >
                      🛰️
                    </div>
                    <div className="image-preview-info">
                      <div className="image-preview-name">{img.filename}</div>
                      <div className="image-preview-meta">
                        {img.metadata?.width}×{img.metadata?.height}
                        {img.metadata?.band_count && ` · ${img.metadata.band_count} bands`}
                        {img.metadata?.crs && ` · ${img.metadata.crs}`}
                      </div>
                      <div className="image-preview-meta">
                        {img.sizeMb} MB · {img.metadata?.format || 'Unknown'}
                        {img.metadata?.is_georeferenced === false && ' · No CRS'}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <QueryInput onSubmit={handleQuery} loading={loading} />

          {error && (
            <div className="warning-banner">⚠️ {error}</div>
          )}
        </div>

        {/* Right Panel */}
        <div className="right-panel">
          {loading ? (
            <div className="card">
              <div className="empty-state">
                <div className="loading-spinner"></div>
                <div className="loading-text">Analyzing...</div>
              </div>
            </div>
          ) : (
            <ResultsPanel result={result} />
          )}
        </div>
      </div>
    </div>
  );
}
