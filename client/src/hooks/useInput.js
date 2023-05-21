import { useState } from "react";

const useInput = (initialValue = "", customOnChange = null) => {
  const [value, setValue] = useState(initialValue);
  const onChange = (e) => {
    setValue(e.target.value);
    if (customOnChange instanceof Function) {
      customOnChange(e);
    }
  };
  return { value, onChange };
};

export default useInput;
