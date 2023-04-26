import "./Input.css";

function Input({ className = "", ...props }) {
  return <input {...props} className={`input ${className}`} />;
}

export default Input;
