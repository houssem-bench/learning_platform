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
            <p>{item.stem}</p>
            <p className="notice">
              Your answer: {item.selected_index !== null ? String.fromCharCode(65 + item.selected_index) : "Unanswered"}
            </p>
            <p className="notice">
              Correct answer: {String.fromCharCode(65 + item.correct_index)}
            </p>
            <div style={{ display: "grid", gap: 8, marginTop: 12 }}>
              {item.options.map((option, optionIndex) => {
                const isCorrect = optionIndex === item.correct_index;
                const isSelected = optionIndex === item.selected_index;
                const className = [
                  "option-result",
                  isCorrect ? "correct" : "",
                  isSelected && !isCorrect ? "wrong" : ""
                ]
                  .filter(Boolean)
                  .join(" ");
                return (
                  <div className={className} key={optionIndex}>
                    <span>
                      {String.fromCharCode(65 + optionIndex)}. {option}
                    </span>
                  </div>
                );
              })}
            </div>
            <p>{item.explanation}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Results;
