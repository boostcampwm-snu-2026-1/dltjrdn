import { useState } from 'react'

function App() {
  // 텍스트 아이디어 입력값
  const [idea, setIdea] = useState('')
  // 업로드한 이미지 미리보기 URL
  const [imageUrl, setImageUrl] = useState(null)

  // 이미지 파일 선택 시 미리보기 생성
  function handleImageChange(e) {
    const file = e.target.files[0]
    if (file) {
      setImageUrl(URL.createObjectURL(file))
    }
  }

  return (
    <main className="container">
      <h1>마크 스킨생성기</h1>

      {/* 사진 업로드 ( + 박스 ) */}
      <div className="field">
        <span>사진 업로드</span>
        <label className="upload-box">
          {imageUrl ? (
            <img className="preview" src={imageUrl} alt="업로드한 이미지 미리보기" />
          ) : (
            <span className="plus">＋</span>
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
    </main>
  )
}

export default App
