import { useState, useRef } from 'react';

/**
 * ImageUploader — Drag-and-drop image upload with preview and metadata.
 */
export default function ImageUploader({ onUpload, sessionId }) {
  const [dragOver, setDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => setDragOver(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) handleFiles(files);
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) handleFiles(files);
  };

  const handleFiles = async (files) => {
    setError(null);
    setUploading(true);

    try {
      for (const file of files) {
        await onUpload(file);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-title">
        <span className="card-title-icon">🛰️</span>
        Upload Images
      </div>

      <div
        className={`upload-zone ${dragOver ? 'drag-over' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="upload-zone-icon">📁</div>
        <div className="upload-zone-text">
          <strong>Click to upload</strong> or drag and drop
        </div>
        <div className="upload-zone-formats">
          GeoTIFF · TIFF · PNG · JPEG
        </div>
        {uploading && (
          <div style={{ marginTop: '12px' }}>
            <div className="loading-spinner" style={{ margin: '0 auto' }}></div>
            <div className="loading-text">Uploading...</div>
          </div>
        )}
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept=".tif,.tiff,.geotiff,.png,.jpg,.jpeg"
        multiple
        onChange={handleFileSelect}
        style={{ display: 'none' }}
        id="image-upload-input"
      />

      {error && (
        <div className="warning-banner" style={{ marginTop: '12px' }}>
          ⚠️ {error}
        </div>
      )}
    </div>
  );
}
