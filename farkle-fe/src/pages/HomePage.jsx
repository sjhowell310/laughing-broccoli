import { useState } from 'react'

function HomePage() {
    const [state, setState] = useState({})  // renamed for clarity

    // Step 1: Create state variables to hold input values
    const [NoOfPlayers, setNoOfPlayers] = useState(2);
    const [OrderDice, setOrderDice] = useState(true);
    const [ScoreLimit, setScoreLimit] = useState(10_000);
    const [ScoreThreshold, setScoreThreshold] = useState(500);
    const [PlayerSpecifySet, setPlayerSpecifySet] = useState(false);

    // Step 2: Function to handle button click
    const configGame = async () => {
        getGame(NoOfPlayers,
        OrderDice,
        ScoreLimit,
        ScoreThreshold,
        PlayerSpecifySet);
    };

    const getGame = async (NoOfPlayers,
        OrderDice,
        ScoreLimit,
        ScoreThreshold,
        PlayerSpecifySet) => {
        await fetch(`http://localhost:9002/game/configure?num_players=${NoOfPlayers}&order_dice=${OrderDice}&score_limit=${ScoreLimit}&score_threshold=${ScoreThreshold}&player_specify_set=${PlayerSpecifySet}`)
    };
    const resetGame = async () => {
        await fetch(`http://localhost:9002/game/reset`)
    };
    const fetchGameState = async () => {
        try {
            const response = await fetch('http://localhost:9002/game/state')
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
                <button onClick={fetchGameState}>
                    Fetch game state
                </button>
                <pre>
                    {JSON.stringify(state, null, 4)}
                </pre>
            </div>
            <h2>Search Form</h2>

            {/* Input for name */}
            <label>
                Number of players:
                <input
                    type="number"
                    value={NoOfPlayers}
                    onChange={(e) => setNoOfPlayers(e.target.value)} // update state on input
                    placeholder="Enter name"
                />
            </label>

            <br /><br />

            {/* Input for city */}
            <label>
                OrderDice:
                <input
                    type="text"
                    value={OrderDice}
                    onChange={(e) => setOrderDice(e.target.value)} // update state on input
                    placeholder="Enter city"
                />
            </label>

            <br /><br />
            {/* Input for name */}
            <label>
                ScoreLimit:
                <input
                    type="text"
                    value={ScoreLimit}
                    onChange={(e) => setScoreLimit(e.target.value)} // update state on input
                    placeholder="Enter name"
                />
            </label>

            <br /><br />

            {/* Input for city */}
            <label>
                ScoreThreshold:
                <input
                    type="text"
                    value={ScoreThreshold}
                    onChange={(e) => setScoreThreshold(e.target.value)} // update state on input
                    placeholder="Enter ScoreThreshold"
                />
            </label>

            <br /><br />
            {/* Input for name */}
            <label>
                PlayerSpecifySet:
                <input
                    type="text"
                    value={PlayerSpecifySet}
                    onChange={(e) => setPlayerSpecifySet(e.target.value)} // update state on input
                    placeholder="Enter name"
                />
            </label>

            <br /><br />

            {/* Button to trigger query */}
            <button onClick={configGame}>Configure Game</button>
            <br /> <br />
            <button onClick={resetGame}>Reset Game</button>
        </>
    )
}

export default HomePage;