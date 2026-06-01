import { useState } from 'react'
import { generateSkin } from '../api/skinApi'

export function useSkinGenerator() {
  const [idea, setIdea] = useState('')
  const [imageFile, setImageFile] = useState(null)
  const [imageUrl, setImageUrl] = useState(null)
  const [prompt, setPrompt] = useState('')
  const [skin, setSkin] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [direct, setDirect] = useState(true)

  function applyImage(file) {
    if (file && file.type.startsWith('image/')) {
      setImageFile(file)
      setImageUrl(URL.createObjectURL(file))
    }
  }

  function removeImage() {
    if (imageUrl) URL.revokeObjectURL(imageUrl)
    setImageFile(null)
    setImageUrl(null)
  }

  async function generate() {
    setError('')
    setPrompt('')
    setSkin('')
    if (!idea && !imageFile) {
      setError('아이디어를 입력하거나 사진을 올려주세요.')
      return
    }
    setLoading(true)
    try {
      const data = await generateSkin({ idea, imageFile, direct })
      setPrompt(data.prompt)
      setSkin(data.image)
      if (!data.valid) {
        setError('스킨 형식 검증 경고: ' + (data.errors || []).join(', '))
      }
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return {
    idea,
    setIdea,
    imageUrl,
    prompt,
    skin,
    loading,
    error,
    direct,
    setDirect,
    applyImage,
    removeImage,
    generate,
  }
}
