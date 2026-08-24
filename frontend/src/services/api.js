/**
 * SatQuery AI — API Service Layer
 *
 * Handles communication with the FastAPI backend.
 */

const API_BASE = '/api';

/**
 * Upload an image file.
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
 */
export async function sendQuery(query, sessionId = null, mode = 'change') {
  const response = await fetch(`${API_BASE}/query/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, session_id: sessionId, mode }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Query failed' }));
    throw new Error(error.detail || 'Query failed');
  }

  return response.json();
}

/**
 * Check backend health and feature status.
 */
export async function getHealth() {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) throw new Error('Backend unavailable');
  return response.json();
}

/**
 * Get detailed system status including module availability.
 */
export async function getSystemStatus() {
  const response = await fetch(`${API_BASE}/status`);
  if (!response.ok) throw new Error('Status check failed');
  return response.json();
}

/**
 * Get supported tasks and scenarios.
 */
export async function getSupportedTasks() {
  const response = await fetch(`${API_BASE}/query/tasks`);
  if (!response.ok) throw new Error('Failed to fetch tasks');
  return response.json();
}

/**
 * Get list of operational scenarios.
 */
export async function getScenarios() {
  const response = await fetch(`${API_BASE}/scenarios/`);
  if (!response.ok) throw new Error('Failed to fetch scenarios');
  return response.json();
}

/**
 * Load a scenario preset into a session.
 */
export async function loadScenario(scenarioId, sessionId = null) {
  const response = await fetch(`${API_BASE}/scenarios/load`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scenario_id: scenarioId, session_id: sessionId }),
  });
  if (!response.ok) throw new Error('Failed to load scenario');
  return response.json();
}
