import SkinViewer3D from './SkinViewer3D'

export default function SkinResult({ skin, prompt }) {
  if (!skin) return null

  return (
    <div className="result">
      <span>생성된 스킨 (3D 미리보기)</span>
      <SkinViewer3D skin={skin} />
      <img className="skin-img" src={skin} alt="스킨 전개도(64×64)" />
      <a className="download-btn" href={skin} download="skin.png">
        ⬇ 다운로드 (PNG)
      </a>
      {prompt && <p className="prompt-text">프롬프트: {prompt}</p>}
    </div>
  )
}
