// src/lib/api.ts

/**
 * A lightweight wrapper around fetch to standardize calling our backend API.
 */
export const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000/api';

/**
 * callApi() is a convenience function that:
 * - prepends the base URL
 * - attaches any required headers or tokens (e.g. for auth)
 * - handles common error flows
 */
export async function callApi(
  endpoint: string,
  options?: RequestInit
): Promise<any> {
  const url = `${API_BASE_URL}${endpoint}`;

  const res = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    // Throwing an error here will let us catch it in a try/catch in the UI
    throw new Error(`API request failed with status ${res.status}`);
  }

  return res.json();
}
