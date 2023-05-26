import { useState } from "react";
import "./Input.scss";

function Input({
  id,
  className,
  onChange,
  onValidation = () => ({
    isValid: true,
  }),
  initialValue = "",
  isTextarea = false,
  type = "text",
  placeholder = "",
  readOnly = false,
}) {
  const [value, setValue] = useState(initialValue);
  const [validationErr, setValidationErr] = useState(null);

  const inputClass = `input${className ? " " + className : ""}${
    validationErr ? " input_invalid" : ""
  }`;

  const onInputChange = (e) => {
    const value = e.target.value;
    setValue(value);

    const validationResult = onValidation(value);
    if (!validationResult.isValid) {
      setValidationErr(validationResult.message);
    } else {
      setValidationErr(null);
    }

    onChange(value);
  };
  return (
    <div className={inputClass}>
      {!isTextarea ? (
        <input
          id={id}
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onInputChange}
          readOnly={readOnly}
        ></input>
      ) : (
        <textarea
          id={id}
          type={type}
          rows={initialValue.split("\n").length || 1}
          placeholder={placeholder}
          value={value}
          onChange={(e) => {
            onInputChange(e);
            e.target.style.height = "auto";
            e.target.style.height = e.target.scrollHeight + "px";
          }}
          readOnly={readOnly}
        ></textarea>
      )}
      {validationErr && (
        <div className="input__validation-error">{validationErr}</div>
      )}
    </div>
  );
}

export default Input;
