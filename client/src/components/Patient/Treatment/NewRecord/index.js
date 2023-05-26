import { useEffect, useState } from "react";

import "./index.scss";

import { RECORDS_URLS } from "../../../../api/endpoints";
import { authorizedAxios } from "../../../../api/axios";
import usePatientId from "../../../../hooks/usePatientId";

import RubricsSelect from "../../../UI/RubricsSelect";
import Input from "../../../UI/Input";
import LoadingSpinner from "../../../UI/Spinner";
import removeIcon from "../../../../assets/cross.svg";

function NewRecord({ onSubmit }) {
  const [controlTitle, setControlTitle] = useState("");
  const [rubricVariants, setRubricVariants] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const { patientId } = usePatientId();

  const setRubricAttr = (id, key, value) => {
    setRubricVariants((rubrics) =>
      rubrics.map((rubric) =>
        rubric.id === id ? { ...rubric, [key]: value } : { ...rubric }
      )
    );
  };

  const validateRubricTitle = (rubricId) => {
    if (
      rubricId === 0 ||
      rubricVariants.filter((variant) => variant.rubricId === rubricId).length <
        2
    ) {
      return { isValid: true };
    }
    return {
      isValid: false,
      message: "Нельзя добавить два изменения для одной рубрики",
    };
  };

  const validateText = (text) => {
    if (text.length < 3) {
      return {
        isValid: false,
        message: "Не меньше 3 символов",
      };
    }
    return { isValid: true };
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
  const submitNewRecord = async () => {
    const rubrics = [];
    for (let i = 0; i < rubricVariants.length; i++) {
      const variant = rubricVariants[i];
      if (variant.description.length < 3) {
        return;
      }
      rubrics.push(variant.rubricId);
    }
    if (rubrics.length > new Set(rubrics).size) {
      return;
    }
    setIsLoading(true);
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
    setControlTitle("");
    setRubricVariants([
      {
        id: Math.random().toString(36).substring(2, 12),
        rubricId: 0,
        description: "",
      },
    ]);
    setIsLoading(false);
    onSubmit();
  };
  useEffect(addRubric, []);
  return (
    <section className="new-record">
      <div className="container">
        <div className="new-record__header">Добавить контроль</div>
        {isLoading ? (
          <LoadingSpinner />
        ) : (
          <>
            <Input
              className="new-record__title"
              type="text"
              placeholder="Название"
              onChange={(value) => setControlTitle(value)}
              onValidation={validateText}
            />
            <div className="new-record__subheader">Изменившиеся рубрики:</div>
            {rubricVariants.map((rubric) => (
              <div className="new-record__rubric" key={rubric.id}>
                <RubricsSelect
                  onSelect={({ rubricId }) =>
                    setRubricAttr(rubric.id, "rubricId", rubricId)
                  }
                  validation={validateRubricTitle(rubric.rubricId)}
                />
                <Input
                  className="new-record__rubric-descr"
                  type="text"
                  placeholder="Опишите изменения"
                  onChange={(value) => {
                    setRubricAttr(rubric.id, "description", value);
                  }}
                  onValidation={validateText}
                  isTextarea
                ></Input>
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
            <button onClick={submitNewRecord} className="new-record__save-btn">
              Сохранить
            </button>
          </>
        )}
      </div>
    </section>
  );
}

export default NewRecord;
