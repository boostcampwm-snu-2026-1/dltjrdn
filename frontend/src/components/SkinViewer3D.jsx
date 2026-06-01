import { useEffect, useRef } from 'react'
import { SkinViewer, IdleAnimation } from 'skinview3d'

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
    viewer.animation = new IdleAnimation()
    viewer.autoRotate = true
    viewer.autoRotateSpeed = 0.6
    viewer.zoom = 0.9

    return () => viewer.dispose()
  }, [skin])

  return <canvas ref={canvasRef} className="skin-3d" />
}
