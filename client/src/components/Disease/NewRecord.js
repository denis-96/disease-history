import { useState } from "react";

import "./NewRecord.scss";

import RubricsSelect from "./RubricsSelect";
import removeIcon from "../../assets/remove.svg";
import { generateId } from "../../utils";

function NewRecord() {
  const [controlName, setControlName] = useState("");
  const [rubrics, setRubrics] = useState([
    {
      id: generateId(),
      title: "",
      content: "",
    },
  ]);

  const setRubricAttr = (value, id, attr) => {
    setRubrics((rubrics) =>
      rubrics.map((rubric) =>
        rubric.id === id ? { ...rubric, [attr]: value } : { ...rubric }
      )
    );
  };

  const addRubric = () => {
    setRubrics((rubrics) => [
      ...rubrics,
      {
        id: generateId(),
        title: "",
        content: "",
      },
    ]);
  };

  const removeRubric = (id) => {
    setRubrics((rubrics) => rubrics.filter((rubric) => rubric.id !== id));
  };

  return (
    <section className="new-record">
      <div className="container">
        <div className="new-record__header">Добавить контроль</div>
        <input
          className="input new-record__title"
          type="text"
          placeholder="Название"
          value={controlName}
          onChange={(e) => setControlName(e.target.value)}
        />
        <div className="new-record__subheader">Изменившиеся рубрики:</div>
        {rubrics.map((rubric) => (
          <div className="new-record__rubric" key={rubric.id}>
            <RubricsSelect
              onSelect={(value) => setRubricAttr(value, rubric.id, "title")}
            />
            <textarea
              className="textarea new-record__rubric-descr"
              type="text"
              rows="1"
              placeholder="Опишите изменения"
              value={rubric.content}
              onChange={(e) =>
                setRubricAttr(e.target.value, rubric.id, "content")
              }
            ></textarea>
            <button
              onClick={() => removeRubric(rubric.id)}
              className="new-record__remove-rubric"
            >
              <img src={removeIcon} alt="remove" />
            </button>
          </div>
        ))}
        <button onClick={addRubric} className="new-record__add-rubric-btn">
          +
        </button>
        <button className="new-record__save-btn">Сохранить</button>
      </div>
    </section>
  );
}

export default NewRecord;
