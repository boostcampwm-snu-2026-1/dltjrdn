export default function IdeaInput({ idea, setIdea, direct, setDirect }) {
  return (
    <>
      <label className="field">
        <span>{direct ? '영어 프롬프트 직접 입력' : '아이디어 입력'}</span>
        <textarea
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          placeholder={
            direct
              ? '예: a green dinosaur in a blue jumpsuit with red gloves'
              : '예: 좀비 해적, 보라색 정장을 입은 마법사'
          }
          rows={3}
        />
      </label>

      <label className="toggle">
        <input
          type="checkbox"
          checked={direct}
          onChange={(e) => setDirect(e.target.checked)}
        />
        Gemini 없이 직접 프롬프트 (임시 · 영어로 입력)
      </label>
    </>
  )
}
