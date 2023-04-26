import "./TextArea.css";

function TextArea({ children, className = "", ...props }) {
  return (
    <textarea {...props} className={`textarea ${className}`}>
      {children}
    </textarea>
  );
}

export default TextArea;
