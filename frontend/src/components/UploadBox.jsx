import { useState } from 'react'

export default function UploadBox({ imageUrl, onApply, onRemove }) {
  const [dragging, setDragging] = useState(false)

  function handleChange(e) {
    onApply(e.target.files[0])
  }

  function handleRemove(e) {
    e.preventDefault()
    e.stopPropagation()
    onRemove()
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragging(false)
    onApply(e.dataTransfer.files[0])
  }

  return (
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
            <button className="remove-btn" onClick={handleRemove} title="사진 제거">
              ✕
            </button>
          </>
        ) : (
          <span className="plus">＋<small>클릭 또는 드래그</small></span>
        )}
        <input type="file" accept="image/*" onChange={handleChange} hidden />
      </label>
    </div>
  )
}
