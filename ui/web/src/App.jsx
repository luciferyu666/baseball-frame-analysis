import { useEffect, useState } from 'react'

export default function App(){
  const [img,setImg]=useState(null)
  useEffect(()=>{
    const ws=new WebSocket(`ws://${location.hostname}:8000/ws/live`)
    ws.onmessage=e=>{
      const data=JSON.parse(e.data)
      setImg(`data:image/jpeg;base64,${data.image}`)
    }
  },[])
  return <div style={{textAlign:'center'}}>
    <h2>Live Pitch Feed</h2>
    {img && <img src={img} width="640"/>}
  </div>
}
