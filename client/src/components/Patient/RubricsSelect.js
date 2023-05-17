import { useState } from "react";

import "./RubricsSelect.scss";

import DropdownIcon from "../../assets/dropdown-arrow.svg";
import Rubrics from "../../rubrics.json";

function RubricsSelect({ onSelect }) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedRubric, setSelectedRubric] = useState("Выберите рубрику");

  const onRubricClick = (e) => {
    setSelectedRubric(e.target.textContent);
    setIsOpen(false);
    onSelect(e.target.textContent);
  };

  const className = `rubrics-select ${isOpen ? "rubrics-select_active" : ""}`;

  return (
    <div className={className}>
      <button
        onClick={() => setIsOpen((isOpen) => !isOpen)}
        className="rubrics-select__btn"
      >
        <span>{selectedRubric}</span>
        <img src={DropdownIcon} alt="arrow" />
      </button>
      <div className="rubrics-select__content">
        <ul className="rubrics-select__list">
          {Rubrics.map((rubric, i) => (
            <li className="rubrics-select__item" key={i}>
              <details>
                <summary>{rubric.rubric}</summary>
                <ul>
                  {rubric.subrubrics.map((subrubric, i) => (
                    <li key={i} onClick={onRubricClick} tabIndex={0}>
                      {subrubric}
                    </li>
                  ))}
                </ul>
              </details>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default RubricsSelect;
