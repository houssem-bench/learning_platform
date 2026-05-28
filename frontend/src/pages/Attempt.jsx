import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";

import { getAttempt, submitAttempt } from "../api.js";
import Timer from "../components/Timer.jsx";

function Attempt() {
  const { attemptId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const storedAttempt = useMemo(() => {
    const saved = sessionStorage.getItem(`attempt:${attemptId}`);
    return saved ? JSON.parse(saved) : null;
  }, [attemptId]);

  const [attempt, setAttempt] = useState(
    location.state?.attempt || storedAttempt
  );
  const [answers, setAnswers] = useState({});
  const [remainingSeconds, setRemainingSeconds] = useState(
    attempt?.remaining_seconds || attempt?.time_limit_seconds || 0
  );
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!attempt) {
      getAttempt(attemptId)
        .then((data) => {
          setAttempt(data);
          setRemainingSeconds(
            data.remaining_seconds || data.time_limit_seconds || 0
          );
          sessionStorage.setItem(
            `attempt:${attemptId}`,
            JSON.stringify(data)
          );
        })
        .catch((err) => setError(err.message || "Failed to load attempt"));
    }
  }, [attempt, attemptId]);

  const handleSelect = (questionId, value) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }));
  };

  const handleSubmit = async () => {
    if (submitting) {
      return;
    }
    setSubmitting(true);
    setError("");
    try {
      const result = await submitAttempt(attemptId, answers);
      sessionStorage.setItem(
        `result:${attemptId}`,
        JSON.stringify(result)
      );
      navigate(`/attempts/${attemptId}/results`, {
        state: { result }
      });
    } catch (err) {
      setError(err.message || "Failed to submit attempt");
    } finally {
      setSubmitting(false);
    }
  };

  if (!attempt) {
    return <div className="card">Loading attempt...</div>;
  }

  return (
    <div>
      <h1>Quiz attempt</h1>
      <Timer remainingSeconds={remainingSeconds} onExpire={handleSubmit} />
      {error ? <p className="notice">{error}</p> : null}
      <div style={{ marginTop: 20, display: "grid", gap: 16 }}>
        {attempt.questions.map((question, index) => (
          <div className="question" key={question.id}>
            <strong>
              Q{index + 1}. {question.stem}
            </strong>
            {question.options.map((option, optionIndex) => (
              <label className="option" key={optionIndex}>
                <input
                  type="radio"
                  name={`q-${question.id}`}
                  value={optionIndex}
                  checked={answers[question.id] === optionIndex}
                  onChange={() => handleSelect(question.id, optionIndex)}
                />
                <span>
                  {String.fromCharCode(65 + optionIndex)}. {option}
                </span>
              </label>
            ))}
          </div>
        ))}
      </div>
      <div style={{ marginTop: 24 }}>
        <button className="button" onClick={handleSubmit} disabled={submitting}>
          {submitting ? "Submitting..." : "Submit answers"}
        </button>
      </div>
    </div>
  );
}

export default Attempt;
