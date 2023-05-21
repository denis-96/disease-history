import { useEffect, useState } from "react";

import "./index.scss";

import { RECORDS_URLS } from "../../../../api/endpoints";
import { authorizedAxios } from "../../../../api/axios";
import usePatientId from "../../../../hooks/usePatientId";

import RubricsSelect from "../../../UI/RubricsSelect";
import removeIcon from "../../../../assets/remove.svg";

function NewRecord({ onSubmit }) {
  const [controlTitle, setControlTitle] = useState("");
  const [rubricVariants, setRubricVariants] = useState([]);
  const [isValidationErr, setIsValidationErr] = useState(true);

  const { patientId } = usePatientId();

  const onTitleChange = (e) => {
    if (e.target.value.length < 3) {
      e.target.classList.add("input_invalid");
    } else {
      e.target.classList.remove("input_invalid");
    }
    setControlTitle(e.target.value);
  };

  const setRubricAttr = (id, key, value) => {
    setRubricVariants((rubrics) =>
      rubrics.map((rubric) =>
        rubric.id === id ? { ...rubric, [key]: value } : { ...rubric }
      )
    );
  };

  const addRubric = () => {
    setRubricVariants((rubrics) => [
      ...rubrics,
      {
        id: Math.random().toString(36).substring(2, 12),
        rubricId: 0,
        description: "",
      },
    ]);
  };

  const removeRubric = (id) => {
    setRubricVariants((rubrics) =>
      rubrics.filter((rubric) => rubric.id !== id)
    );
  };

  useEffect(() => {
    const rubrics = [];
    for (const variant of rubricVariants) {
      if (!variant.rubricId || variant.description.length < 3) {
        setIsValidationErr(true);
        return;
      }
      rubrics.push(+variant.rubricId);
    }
    if (rubrics.length > new Set(rubrics).size || controlTitle.length < 3) {
      setIsValidationErr(true);
      return;
    }
    setIsValidationErr(false);
  }, [rubricVariants, controlTitle]);

  const submitNewRecord = async () => {
    await authorizedAxios.post(
      RECORDS_URLS.RECORD,
      JSON.stringify({
        title: controlTitle,
        rubrics: rubricVariants.map((rubric) => ({
          description: rubric.description,
          rubric_id: rubric.rubricId,
        })),
        patient_id: patientId,
      })
    );
    setRubricVariants([
      {
        id: Math.random().toString(36).substring(2, 12),
        rubricId: 0,
        description: "",
      },
    ]);
    setControlTitle("");
    onSubmit();
  };

  useEffect(addRubric, []);

  return (
    <section className="new-record">
      <div className="container">
        <div className="new-record__header">Добавить контроль</div>
        <input
          className="input new-record__title"
          type="text"
          placeholder="Название"
          value={controlTitle}
          onChange={onTitleChange}
        />
        {/* <div className="input-error new-record__title-error">
          Не меньше трёх символов
        </div> */}
        <div className="new-record__subheader">Изменившиеся рубрики:</div>
        {rubricVariants.map((rubric) => (
          <div className="new-record__rubric" key={rubric.id}>
            <RubricsSelect
              onSelect={(rubricId) =>
                setRubricAttr(rubric.id, "rubricId", rubricId)
              }
            />
            <textarea
              className="textarea new-record__rubric-descr"
              type="text"
              rows="1"
              placeholder="Опишите изменения"
              value={rubric.content}
              onChange={(e) => {
                setRubricAttr(rubric.id, "description", e.target.value);
              }}
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
        <button
          onClick={submitNewRecord}
          className="new-record__save-btn"
          disabled={isValidationErr}
        >
          Сохранить
        </button>
      </div>
    </section>
  );
}

export default NewRecord;
