import UploadBox from './components/UploadBox'
import IdeaInput from './components/IdeaInput'
import SkinResult from './components/SkinResult'
import { useSkinGenerator } from './hooks/useSkinGenerator'

function App() {
  const {
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
  } = useSkinGenerator()

  return (
    <main className="container">
      <h1>마크 스킨생성기</h1>

      <UploadBox imageUrl={imageUrl} onApply={applyImage} onRemove={removeImage} />

      <IdeaInput idea={idea} setIdea={setIdea} direct={direct} setDirect={setDirect} />

      <button className="generate-btn" onClick={generate} disabled={loading}>
        {loading ? '스킨 생성 중… (수십 초)' : '스킨 생성'}
      </button>

      {error && <p className="error">{error}</p>}

      <SkinResult skin={skin} prompt={prompt} />
    </main>
  )
}

export default App
