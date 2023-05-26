import { useEffect, useRef, useState } from "react";

import "./RubricsSelect.scss";

import DropdownIcon from "../../assets/dropdown-arrow.svg";
import { RUBRICS_URLS } from "../../api/endpoints";
import useAuthorizedAxios from "../../hooks/useAuthorizedAxios";

function RubricsSelect({ onSelect, validation = { isValid: true } }) {
  const [rubrics, setRubrics] = useState([]);

  const [isOpen, setIsOpen] = useState(false);
  const [selectedRubric, setSelectedRubric] = useState({});
  const mainRef = useRef();

  const authorizedAxios = useAuthorizedAxios();

  const closeDropdown = (e) => {
    if (mainRef.current && isOpen && !mainRef.current.contains(e.target)) {
      setIsOpen(false);
    }
  };

  const onRubricClick = (e) => {
    const rubric = {
      rubricId: e.target.getAttribute("data-rubric-id"),
      title: e.target.textContent,
    };
    setSelectedRubric(rubric);
    setIsOpen(false);
    onSelect(rubric);
  };

  useEffect(() => {
    const getRubrics = async () => {
      const response = await authorizedAxios.get(RUBRICS_URLS.ALL);
      setRubrics(response.data);
    };
    getRubrics();
    // eslint-disable-next-line
  }, []);
  useEffect(() => {
    isOpen && document.body.addEventListener("mousedown", closeDropdown);
    return () => {
      document.body.removeEventListener("mousedown", closeDropdown);
    };
    // eslint-disable-next-line
  }, [isOpen]);

  const className = `rubrics-select${isOpen ? " rubrics-select_active" : ""} ${
    !validation.isValid ? " rubrics-select_invalid" : ""
  }`;

  return (
    <div className={className} ref={mainRef}>
      <button
        className="rubrics-select__btn"
        onClick={() => setIsOpen((isOpen) => !isOpen)}
      >
        <span>{selectedRubric.title || "Выберите рубрику"}</span>
        <img src={DropdownIcon} alt="arrow" />
      </button>
      <div className="rubrics-select__content">
        <ul className="rubrics-select__list">
          {rubrics?.length ? (
            rubrics.map((rubric) => (
              <li className="rubrics-select__item" key={rubric.id}>
                <details>
                  <summary>{rubric.title}</summary>
                  <ul>
                    {rubric.rubrics.map((subrubric) => (
                      <li
                        key={subrubric.id}
                        onClick={onRubricClick}
                        data-rubric-id={subrubric.id}
                        tabIndex={0}
                      >
                        {subrubric.title}
                      </li>
                    ))}
                  </ul>
                </details>
              </li>
            ))
          ) : (
            <div className="rubrics-select__no-rubrics">Нет рубрик</div>
          )}
        </ul>
      </div>
      {!validation.isValid && (
        <div className="rubrics-select__validation-error">
          {validation.message}
        </div>
      )}
    </div>
  );
}

export default RubricsSelect;
