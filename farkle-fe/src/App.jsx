import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [state, setState] = useState({})  // renamed for clarity

  const fetchGameState = async () => {
    try {
      const response = await fetch('http://localhost:9002/game/start?num_players=2&order_dice=false&score_limit=10000&score_threshold=500&player_specify_set=false')
      console.log(response);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }
      const data = await response.json()   // parse JSON
      console.log(data)
      setState(data)                       // update React state
    } catch (error) {
      console.error('Error fetching game state:', error)
      setState({ error: error.message })
    }
  }

  return (
    <>
      <div>
        <h1>An attempt at a farkle game in browser</h1>
      </div>
      <div className="card">
        <button onClick={() => setCount(count => count + 1)}>
          count is {count}s innit
        </button>

        <button onClick={fetchGameState}>
          Fetch game state
        </button>

        <pre>
          {JSON.stringify(state, null, 2)}
        </pre>

        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>

      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
