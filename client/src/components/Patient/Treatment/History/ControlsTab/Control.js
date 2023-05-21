import { useState } from "react";

import "./Control.scss";

import { RECORDS_URLS } from "../../../../../api/endpoints";
import useAuthorizedAxios from "../../../../../hooks/useAuthorizedAxios";

import RubricsSelect from "../../../../UI/RubricsSelect";
import editIcon from "../../../../../assets/edit.svg";
import applyIcon from "../../../../../assets/apply.svg";

function Control({ id, title, date, rubrics, toggleSelect }) {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [editMode, setEditMode] = useState(false);

  const [newRubrics, setNewRubrics] = useState([]);
  const [changedRubrics, setChangedRubrics] = useState({});

  const authorizedAxios = useAuthorizedAxios();

  const contentClass = `control-record__content ${
    isOpen ? "control-record__content_open" : ""
  }`;

  const updateTextareaHeight = (el) => {
    el.style.height = "auto";
    el.style.height = el.scrollHeight + "px";
  };

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

  const onRubricChange = (id, rubricId, e) => {
    setChangedRubrics((rubrics) => ({
      ...rubrics,
      [id]: { rubricId, description: e.target.value },
    }));

    updateTextareaHeight(e.target);
  };

  const transformRubricsData = (rubrics) => {
    return rubrics.map((rubric) => ({
      rubric_id: rubric.rubricId,
      description: rubric.description,
    }));
  };

  const saveChanges = async () => {
    const requestData = {
      rubrics: [].concat(
        transformRubricsData(newRubrics),
        transformRubricsData(Object.values(changedRubrics))
      ),
    };
    authorizedAxios.patch(
      `${RECORDS_URLS.RECORD}?record_id=${id}`,
      JSON.stringify(requestData)
    );
  };

  const toggleEditMode = () => {
    setEditMode((editMode) => {
      if (editMode) {
        console.log("saving changes...");
        saveChanges();
        setNewRubrics([]);
        setChangedRubrics({});
      }
      return !editMode;
    });
  };

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
          <button className="control-record__edit-btn" onClick={toggleEditMode}>
            {editMode ? (
              <img src={applyIcon} alt="save chages" />
            ) : (
              <img src={editIcon} alt="edit" />
            )}
          </button>
          {rubrics.map((rubric, i) => (
            <div className="control-record__rubric" key={rubric.id}>
              <div className="control-record__rubric-title">
                {i + 1}. {rubric.rubric.title}
              </div>

              <textarea
                className="control-record__rubric-descr textarea"
                value={
                  typeof changedRubrics[rubric.id]?.description !== "undefined"
                    ? changedRubrics[rubric.id]?.description
                    : rubric.description
                }
                rows={rubric.description.split("\n").length}
                onChange={(e) => onRubricChange(rubric.id, rubric.rubric.id, e)}
                readOnly={!editMode}
              />

              {/* <div className="control-record__status-msg">Сохранено</div> */}
            </div>
          ))}
          {editMode &&
            newRubrics.map((rubric, i) => (
              <div className="control-record__rubric" key={rubric.id}>
                <div className="control-record__rubric-title control-record__rubric-title_new">
                  <RubricsSelect
                    onSelect={(rubricId) =>
                      setNewRubricAttr(rubric.id, "rubricId", +rubricId)
                    }
                  />
                </div>

                <textarea
                  className="control-record__rubric-descr textarea"
                  value={rubric.description}
                  rows={rubric.description.split("\n").length}
                  onChange={(e) => {
                    setNewRubricAttr(rubric.id, "description", e.target.value);
                    updateTextareaHeight(e.target);
                  }}
                />

                {/* <div className="control-record__status-msg">Сохранено</div> */}
              </div>
            ))}
          {editMode && (
            <button
              className="control-record__add-rubric-btn"
              onClick={addNewRubric}
            >
              Добавить рубрику
            </button>
          )}
        </div>
      </div>
    </li>
  );
}

export default Control;
