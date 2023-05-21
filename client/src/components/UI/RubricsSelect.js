import { useEffect, useRef, useState } from "react";

import "./RubricsSelect.scss";

import DropdownIcon from "../../assets/dropdown-arrow.svg";
import { RUBRICS_URLS } from "../../api/endpoints";
import useAuthorizedAxios from "../../hooks/useAuthorizedAxios";

function RubricsSelect({ onSelect }) {
  const [rubrics, setRubrics] = useState([]);

  const [isOpen, setIsOpen] = useState(false);
  const [selectedRubric, setSelectedRubric] = useState("Выберите рубрику");
  const mainRef = useRef();

  const authorizedAxios = useAuthorizedAxios();

  const closeDropdown = (e) => {
    if (mainRef.current && isOpen && !mainRef.current.contains(e.target)) {
      setIsOpen(false);
    }
  };

  const onRubricClick = (e) => {
    setSelectedRubric(e.target.textContent);
    setIsOpen(false);

    onSelect(e.target.getAttribute("data-rubric-id"), e.target.textContent);
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

  const className = `rubrics-select ${isOpen ? "rubrics-select_active" : ""}`;

  return (
    <div className={className} ref={mainRef}>
      <button
        className="rubrics-select__btn"
        onClick={() => setIsOpen((isOpen) => !isOpen)}
      >
        <span>{selectedRubric}</span>
        <img src={DropdownIcon} alt="arrow" />
      </button>
      <div className="rubrics-select__content">
        <ul className="rubrics-select__list">
          {rubrics?.length &&
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
            ))}
        </ul>
      </div>
    </div>
  );
}

export default RubricsSelect;
