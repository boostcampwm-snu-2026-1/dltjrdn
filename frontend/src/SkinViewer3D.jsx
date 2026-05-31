import { useEffect, useRef } from 'react'
import { SkinViewer, IdleAnimation } from 'skinview3d'

// 생성된 스킨 PNG(dataURL)를 3D 캐릭터로 렌더링 (마인크래프트에서 보이는 모습)
export default function SkinViewer3D({ skin }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    if (!skin || !canvasRef.current) return

    const viewer = new SkinViewer({
      canvas: canvasRef.current,
      width: 280,
      height: 360,
      skin,
    })
    viewer.animation = new IdleAnimation() // 가볍게 숨쉬는 동작
    viewer.autoRotate = true // 자동 회전
    viewer.autoRotateSpeed = 0.6
    viewer.zoom = 0.9

    // 언마운트/스킨 변경 시 정리 (WebGL 리소스 해제)
    return () => viewer.dispose()
  }, [skin])

  return <canvas ref={canvasRef} className="skin-3d" />
}
