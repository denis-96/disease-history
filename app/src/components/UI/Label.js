import "./Label.css";

function Label({ children, className = "", ...props }) {
  return (
    <label {...props} className={`label ${className}`}>
      {children}
    </label>
  );
}

export default Label;
