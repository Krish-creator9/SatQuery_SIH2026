/**
 * SatQuery AI — API Service Layer
 *
 * All communication with the FastAPI backend goes through here.
 */

const API_BASE = '/api';

/**
 * Upload an image file.
 * @param {File} file - The image file to upload
 * @param {string} imageType - "optical", "sar", "multispectral", "unknown"
 * @param {string} role - "primary", "secondary", "before", "after"
 * @param {string|null} sessionId - Existing session ID (null to create new)
 * @returns {Promise<object>} Upload response with session_id, image_id, metadata
 */
export async function uploadImage(file, imageType = 'unknown', role = 'primary', sessionId = null) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('image_type', imageType);
  formData.append('role', role);
  if (sessionId) {
    formData.append('session_id', sessionId);
  }

  const response = await fetch(`${API_BASE}/upload/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(error.detail || 'Upload failed');
  }

  return response.json();
}

/**
 * Send a natural-language query for analysis.
 * @param {string} query - The user's question
 * @param {string|null} sessionId - Session with uploaded images
 * @returns {Promise<object>} FusedResult with answer, confidence, evidence, trace
 */
export async function sendQuery(query, sessionId = null) {
  const response = await fetch(`${API_BASE}/query/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, session_id: sessionId }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Query failed' }));
    throw new Error(error.detail || 'Query failed');
  }

  return response.json();
}

/**
 * Check backend health and feature status.
 * @returns {Promise<object>} Health status
 */
export async function getHealth() {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) throw new Error('Backend unavailable');
  return response.json();
}

/**
 * Get detailed system status including module availability.
 * @returns {Promise<object>} System status
 */
export async function getSystemStatus() {
  const response = await fetch(`${API_BASE}/status`);
  if (!response.ok) throw new Error('Status check failed');
  return response.json();
}

/**
 * Get list of supported task types.
 * @returns {Promise<object>} Available tasks
 */
export async function getSupportedTasks() {
  const response = await fetch(`${API_BASE}/query/tasks`);
  if (!response.ok) throw new Error('Failed to fetch tasks');
  return response.json();
}
