import { useState } from "react";

import "./index.scss";

import { authorizedAxios } from "../../../../../api/axios";

import Control from "./Control";
import ControlCompare from "../../../../Modals/ControlCompare";
import { RECORDS_URLS } from "../../../../../api/endpoints";
import LoadingSpinner from "../../../../UI/Spinner";

function ControlsTab({ controls, onUpdate }) {
  const [selectedControls, setSelectedControls] = useState([]);
  const [isComparing, setIsComparing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const toggleControlSelect = (control) => {
    const newSelectedControls = selectedControls.filter(
      (item) => item.id !== control.id
    );
    if (newSelectedControls.length === selectedControls.length)
      newSelectedControls.push(control);
    setSelectedControls(newSelectedControls);
  };

  const deleteControls = async () => {
    setIsLoading(true);
    for (const control of selectedControls) {
      await authorizedAxios.delete(
        `${RECORDS_URLS.RECORD}?record_id=${control.id}`
      );
    }
    setSelectedControls([]);
    await onUpdate();
    setIsLoading(false);
  };

  if (isComparing) document.body.style.overflowY = "hidden";
  else document.body.style.overflowY = null;

  return (
    <div className="disease-history__content">
      <div className="disease-history__tool-bar">
        <div className="disease-history__tool-bar-btns">
          <button
            onClick={() => setIsComparing(true)}
            className="disease-history__tool-bar-btn"
            disabled={selectedControls.length !== 2}
          >
            Сравнить
          </button>
          <button
            className="disease-history__tool-bar-btn"
            disabled={selectedControls.length !== 1}
          >
            Изменить
          </button>
          <button
            onClick={deleteControls}
            className="disease-history__tool-bar-btn"
            disabled={selectedControls.length <= 0}
          >
            Удалить
          </button>
        </div>
      </div>

      <ul className="disease-history__timeline">
        {isLoading ? (
          <LoadingSpinner />
        ) : controls?.length ? (
          controls.map((control) => (
            <Control
              {...control}
              toggleSelect={() => toggleControlSelect(control)}
              key={control.id}
            />
          ))
        ) : (
          <p className="disease-history__no-controls">
            Вы пока не добавили ни одного контроля
          </p>
        )}
      </ul>
      {isComparing && (
        <>
          <ControlCompare
            firstControl={selectedControls[0]}
            secondControl={selectedControls[1]}
            onClose={() => setIsComparing(false)}
          />
        </>
      )}
    </div>
  );
}

export default ControlsTab;
