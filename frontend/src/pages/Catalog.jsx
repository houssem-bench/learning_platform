import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { listQuizzes, startAttempt } from "../api.js";

function Catalog() {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    listQuizzes()
      .then((data) => setQuizzes(data))
      .catch((err) => setError(err.message || "Failed to load quizzes"))
      .finally(() => setLoading(false));
  }, []);

  const handleStart = async (quizId) => {
    setError("");
    try {
      const attempt = await startAttempt(quizId);
      sessionStorage.setItem(
        `attempt:${attempt.attempt_id}`,
        JSON.stringify(attempt)
      );
      navigate(`/attempts/${attempt.attempt_id}`, { state: { attempt } });
    } catch (err) {
      setError(err.message || "Failed to start attempt");
    }
  };

  if (loading) {
    return <div className="card">Loading quizzes...</div>;
  }

  return (
    <div>
      <h1>Quiz catalog</h1>
      <p className="notice">
        Select a quiz to begin. Each attempt is timed and explanations appear after
        submission.
      </p>
      {error ? <p className="notice">{error}</p> : null}
      <div className="grid">
        {quizzes.map((quiz) => (
          <div className="card" key={quiz.id}>
            <h3>{quiz.title}</h3>
            <p className="notice">{quiz.description}</p>
            <p className="notice">
              {quiz.question_count} questions · {Math.round(
                quiz.time_limit_seconds / 60
              )} min
            </p>
            <button className="button" onClick={() => handleStart(quiz.id)}>
              Start quiz
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Catalog;
