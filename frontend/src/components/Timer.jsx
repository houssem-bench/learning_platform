import { useEffect, useState } from "react";

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

function Timer({ remainingSeconds, onExpire }) {
  const [seconds, setSeconds] = useState(remainingSeconds);

  useEffect(() => {
    setSeconds(remainingSeconds);
  }, [remainingSeconds]);

  useEffect(() => {
    if (seconds <= 0) {
      if (onExpire) {
        onExpire();
      }
      return undefined;
    }
    const handle = setInterval(() => {
      setSeconds((value) => value - 1);
    }, 1000);
    return () => clearInterval(handle);
  }, [seconds, onExpire]);

  return (
    <div className="timer">
      <span>Time left:</span>
      <span>{formatTime(Math.max(seconds, 0))}</span>
    </div>
  );
}

export default Timer;
