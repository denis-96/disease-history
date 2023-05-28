import { useState } from "react";

import "./Control.scss";

import { RECORDS_URLS } from "../../../../../api/endpoints";
import useAuthorizedAxios from "../../../../../hooks/useAuthorizedAxios";

import RubricsSelect from "../../../../UI/RubricsSelect";
import LoadingSpinner from "../../../../UI/Spinner";
import Input from "../../../../UI/Input";
import editIcon from "../../../../../assets/edit.svg";
import applyIcon from "../../../../../assets/apply.svg";
import crossIcon from "../../../../../assets/cross.svg";
import plusIcon from "../../../../../assets/plus.svg";

function Control({ id, title, date, rubrics, toggleSelect, onUpdate }) {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [editMode, setEditMode] = useState(false);

  const [newRubrics, setNewRubrics] = useState([]);
  const [changedRubrics, setChangedRubrics] = useState({});

  const authorizedAxios = useAuthorizedAxios();

  const contentClass = `control-record__content ${
    isOpen ? "control-record__content_open" : ""
  }`;

  const addNewRubric = () => {
    setNewRubrics((rubrics) => [
      ...rubrics,
      {
        id: Math.random().toString(36).substring(2, 12),
        rubricId: 0,
        description: "",
      },
    ]);
  };

  const setNewRubricAttr = (id, key, value) => {
    setNewRubrics((rubrics) =>
      rubrics.map((rubric) =>
        rubric.id === id ? { ...rubric, [key]: value } : { ...rubric }
      )
    );
  };

  const onRubricChange = (id, rubricId, value) => {
    setChangedRubrics((rubrics) => ({
      ...rubrics,
      [id]: { rubricId, description: value },
    }));
  };

  const validateRubricTitle = (rubricId) => {
    const allRubrics = [].concat(
      rubrics.map((rubric) => ({ rubricId: rubric.rubric.id })),
      newRubrics
    );
    if (
      rubricId === 0 ||
      allRubrics.filter((variant) => variant.rubricId === rubricId).length < 2
    ) {
      return { isValid: true };
    }
    return {
      isValid: false,
      message: "Нельзя добавить два изменения для одной рубрики",
    };
  };

  const validateRubricDescr = (descr) => {
    if (descr.length < 3) {
      return {
        isValid: false,
        message: "Не меньше 3 символов",
      };
    }
    return { isValid: true };
  };

  const transformRubricsData = (rubrics) => {
    return rubrics.map((rubric) => ({
      rubric_id: rubric.rubricId,
      description: rubric.description,
    }));
  };
  const cancelChanges = () => {
    setNewRubrics([]);
    setChangedRubrics({});
    setEditMode(!editMode);
  };

  const saveChanges = async () => {
    const rubricsIds = [].concat(
      rubrics.map((rubric) => rubric.rubric.id),
      newRubrics.map((rubric) => rubric.rubricId)
    );
    if (rubricsIds.length > new Set(rubricsIds).size) {
      return;
    }
    const rubricsToSave = [].concat(
      transformRubricsData(newRubrics),
      transformRubricsData(Object.values(changedRubrics))
    );
    for (let i = 0; i < rubricsToSave.length; i++) {
      if (rubricsToSave[i].description.length < 3) return;
    }

    const requestData = {
      rubrics: rubricsToSave,
    };
    setIsLoading(true);
    await authorizedAxios.patch(
      `${RECORDS_URLS.RECORD}?record_id=${id}`,
      JSON.stringify(requestData)
    );
    setNewRubrics([]);
    setChangedRubrics({});
    setEditMode(!editMode);
    await onUpdate();
    setIsLoading(false);
  };

  return (
    <li className="control-record">
      <div className="control-record__date">
        {new Date(date + "Z").toLocaleString("en-GB", {
          dateStyle: "short",
          timeStyle: "short",
          hour12: false,
        })}
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
            <div className="control-record__title-text">{title}</div>
          </div>
        </div>
        <div className="control-record__body">
          {isLoading && <LoadingSpinner className="control-record__loading" />}

          {editMode ? (
            <>
              <button
                className="control-record__cancel-btn"
                onClick={cancelChanges}
                disabled={isLoading}
              >
                <img src={crossIcon} alt="cancel chages" />
              </button>
              <button
                className="control-record__save-btn"
                onClick={saveChanges}
                disabled={isLoading}
              >
                <img src={applyIcon} alt="save chages" />
              </button>
            </>
          ) : (
            <button
              className="control-record__edit-btn"
              onClick={() => setEditMode(true)}
              disabled={isLoading}
            >
              <img src={editIcon} alt="edit" />
            </button>
          )}
          {rubrics.map((rubric, i) => (
            <div className="control-record__rubric" key={rubric.id}>
              <div className="control-record__rubric-title">
                {i + 1}. {rubric.rubric.title}
              </div>

              <Input
                className="control-record__rubric-descr"
                onChange={(value) =>
                  onRubricChange(rubric.id, rubric.rubric.id, value)
                }
                onValidation={validateRubricDescr}
                initialValue={rubric.description}
                readOnly={!editMode}
                isTextarea
              />

              {/* <div className="control-record__status-msg">Сохранено</div> */}
            </div>
          ))}
          {editMode &&
            newRubrics.map((rubric) => (
              <div className="control-record__rubric" key={rubric.id}>
                <div className="control-record__rubric-title control-record__rubric-title_new">
                  <RubricsSelect
                    onSelect={({ rubricId }) =>
                      setNewRubricAttr(rubric.id, "rubricId", +rubricId)
                    }
                    validation={validateRubricTitle(rubric.rubricId)}
                  />
                </div>

                <Input
                  className="control-record__rubric-descr"
                  onChange={(value) => {
                    setNewRubricAttr(rubric.id, "description", value);
                  }}
                  onValidation={validateRubricDescr}
                  isTextarea
                />

                {/* <div className="control-record__status-msg">Сохранено</div> */}
              </div>
            ))}
          {editMode && (
            <button
              className="control-record__add-rubric-btn"
              onClick={addNewRubric}
              disabled={isLoading}
            >
              <img src={plusIcon} alt="add rubric" />
            </button>
          )}
        </div>
      </div>
    </li>
  );
}

export default Control;
