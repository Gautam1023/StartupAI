
import { useState } from "react";
import axios from "axios";

function App() {

  const [idea, setIdea] = useState("");
  const [funding, setFunding] = useState("");
  const [team, setTeam] = useState("");

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  const evaluateStartup = async () => {

    try {

      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:5000/evaluate",
        {
          idea,
          funding,
          team
        }
      );

      setResult(response.data);

    } catch (error) {

      console.error(error);

      alert("Failed to connect to API");

    } finally {

      setLoading(false);

    }
  };

  return (

    <div
      style={{
        padding: "30px",
        maxWidth: "1200px",
        margin: "auto"
      }}
    >

      <h1>🚀 StartupAI</h1>

      <input
        type="text"
        placeholder="Startup Idea"
        value={idea}
        onChange={(e) => setIdea(e.target.value)}
        style={{
          width: "100%",
          padding: "10px"
        }}
      />

      <br /><br />

      <input
        type="text"
        placeholder="Funding Available"
        value={funding}
        onChange={(e) => setFunding(e.target.value)}
        style={{
          width: "100%",
          padding: "10px"
        }}
      />

      <br /><br />

      <input
        type="text"
        placeholder="Team Size"
        value={team}
        onChange={(e) => setTeam(e.target.value)}
        style={{
          width: "100%",
          padding: "10px"
        }}
      />

      <br /><br />

      <button
        onClick={evaluateStartup}
        style={{
          padding: "12px 25px",
          cursor: "pointer"
        }}
      >
        {loading
          ? "Analyzing..."
          : "Evaluate Startup"}
      </button>

      <hr />

      {result && (

        <>

          <h2>Success Prediction</h2>

          <pre
            style={{
              background: "#f4f4f4",
              padding: "15px",
              borderRadius: "10px"
            }}
          >
            {JSON.stringify(
              result.success_prediction,
              null,
              2
            )}
          </pre>

          <h2>Master Startup Analysis</h2>

          <pre
            style={{
              whiteSpace: "pre-wrap",
              textAlign: "left",
              background: "#f4f4f4",
              padding: "15px",
              borderRadius: "10px"
            }}
          >
            {result.master_report}
          </pre>

        </>

      )}

    </div>

  );
}

export default App;

