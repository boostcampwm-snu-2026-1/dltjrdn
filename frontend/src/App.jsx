import { useState } from 'react'

// 백엔드 주소 (FastAPI dev 서버)
const API = 'http://localhost:8000'

function App() {
  // 텍스트 아이디어 입력값
  const [idea, setIdea] = useState('')
  // 업로드한 이미지 파일 + 미리보기 URL
  const [imageFile, setImageFile] = useState(null)
  const [imageUrl, setImageUrl] = useState(null)
  // 생성된 프롬프트 / 로딩 / 에러
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  // 드래그 중 여부 (박스 강조용)
  const [dragging, setDragging] = useState(false)

  // 이미지 파일 적용 (파일 선택 / 드래그앤드롭 공통)
  function applyImage(file) {
    if (file && file.type.startsWith('image/')) {
      setImageFile(file)
      setImageUrl(URL.createObjectURL(file))
    }
  }

  // 파일 선택창에서 고를 때
  function handleImageChange(e) {
    applyImage(e.target.files[0])
  }

  // 업로드한 사진 제거
  function handleRemoveImage(e) {
    e.preventDefault() // label 클릭으로 파일창 열리는 것 방지
    e.stopPropagation()
    if (imageUrl) URL.revokeObjectURL(imageUrl) // 미리보기 메모리 해제
    setImageFile(null)
    setImageUrl(null)
  }

  // 드래그앤드롭
  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    applyImage(e.dataTransfer.files[0])
  }

  // 프롬프트 생성 요청
  async function handleGenerate() {
    setError('')
    setPrompt('')
    if (!idea && !imageFile) {
      setError('아이디어를 입력하거나 사진을 올려주세요.')
      return
    }
    setLoading(true)
    try {
      const form = new FormData()
      if (idea) form.append('idea', idea)
      if (imageFile) form.append('image', imageFile)

      const res = await fetch(`${API}/generate-prompt`, {
        method: 'POST',
        body: form,
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || '요청 실패')
      setPrompt(data.prompt)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container">
      <h1>마크 스킨생성기</h1>

      {/* 사진 업로드 ( + 박스 ) */}
      <div className="field">
        <span>사진 업로드</span>
        <label
          className={dragging ? 'upload-box dragging' : 'upload-box'}
          onDragOver={(e) => {
            e.preventDefault()
            setDragging(true)
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
        >
          {imageUrl ? (
            <>
              <img className="preview" src={imageUrl} alt="업로드한 이미지 미리보기" />
              <button
                className="remove-btn"
                onClick={handleRemoveImage}
                title="사진 제거"
              >
                ✕
              </button>
            </>
          ) : (
            <span className="plus">＋<small>클릭 또는 드래그</small></span>
          )}
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            hidden
          />
        </label>
      </div>

      {/* 텍스트 아이디어 입력 */}
      <label className="field">
        <span>아이디어 입력</span>
        <textarea
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          placeholder="예: 좀비 해적, 보라색 정장을 입은 마법사"
          rows={3}
        />
      </label>

      <button className="generate-btn" onClick={handleGenerate} disabled={loading}>
        {loading ? '생성 중…' : '프롬프트 생성 (테스트)'}
      </button>

      {error && <p className="error">{error}</p>}

      {prompt && (
        <div className="result">
          <span>생성된 프롬프트</span>
          <p>{prompt}</p>
        </div>
      )}
    </main>
  )
}

export default App
