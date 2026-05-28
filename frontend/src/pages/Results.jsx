import { useMemo } from "react";
import { useLocation, useParams } from "react-router-dom";

function Results() {
  const { attemptId } = useParams();
  const location = useLocation();

  const result = useMemo(() => {
    if (location.state?.result) {
      return location.state.result;
    }
    const saved = sessionStorage.getItem(`result:${attemptId}`);
    return saved ? JSON.parse(saved) : null;
  }, [attemptId, location.state]);

  if (!result) {
    return <div className="card">Result not found.</div>;
  }

  return (
    <div>
      <h1>Results</h1>
      <div className="card">
        <h2>
          Score: {result.correct_count}/{result.total}
        </h2>
        {result.timed_out ? (
          <p className="notice">Time limit exceeded for this attempt.</p>
        ) : null}
      </div>
      <div style={{ marginTop: 20, display: "grid", gap: 16 }}>
        {result.explanations.map((item, index) => (
          <div className="card" key={item.question_id}>
            <strong>Question {index + 1}</strong>
            <p className="notice">
              Your answer: {item.selected_index !== null ? String.fromCharCode(65 + item.selected_index) : "Unanswered"}
            </p>
            <p className="notice">
              Correct answer: {String.fromCharCode(65 + item.correct_index)}
            </p>
            <p>{item.explanation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Results;
