const API = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '')

export async function generateSkin({ idea, imageFile, direct }) {
  const form = new FormData()
  if (idea) form.append('idea', idea)
  if (imageFile) form.append('image', imageFile)
  form.append('direct', direct)

  const res = await fetch(`${API}/generate`, {
    method: 'POST',
    body: form,
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || '요청 실패')
  return data
}
