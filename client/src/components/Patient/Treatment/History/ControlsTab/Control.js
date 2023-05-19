import { useState } from "react";
import "./Control.scss";

function Control({ id, title, date, rubrics, toggleSelect }) {
  const [isOpen, setIsOpen] = useState(false);

  const contentClass = `control-record__content ${
    isOpen ? "control-record__content_open" : ""
  }`;

  return (
    <li className="control-record">
      <div className="control-record__date">
        {new Date(date + "Z").toString()}
      </div>
      <div className={contentClass}>
        <div className="control-record__head">
          <input
            onChange={toggleSelect}
            className="control-record__checkbox"
            type="checkbox"
          />
          <div
            onClick={() => setIsOpen((isOpen) => !isOpen)}
            className="control-record__title"
          >
            {title}
          </div>
        </div>
        <div className="control-record__body">
          {rubrics.map((rubric, i) => (
            <div className="control-record__rubric" key={rubric.id}>
              <div className="control-record__rubric-title">
                {i + 1}. {rubric.rubric.title}
              </div>
              <div className="control-record__rubric-descr textarea">
                {rubric.description}
              </div>
              {/* <div className="control-record__rubric-status-msg">Сохранено</div> */}
            </div>
          ))}
        </div>
      </div>
    </li>
  );
}

export default Control;
