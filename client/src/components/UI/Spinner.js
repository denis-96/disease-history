import "./Spinner.scss";

export default function LoadingSpinner({ className }) {
  return (
    <div className={`loading-spinner ${className ? className : ""}`}></div>
  );
}
