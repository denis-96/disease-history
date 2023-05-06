import { useState } from "react";

import "./ControlsTab.scss";

import Control from "../Records/Control";
import controls from "../../../../controls.json";
import ControlCompare from "../../../Modals/ControlCompare";

function ControlsTab() {
  const [selectedControls, setSelectedControls] = useState([]);
  const [isComparing, setIsComparing] = useState(false);

  const toggleControlSelect = (control) => {
    const newSelectedControls = selectedControls.filter(
      (item) => item.id !== control.id
    );
    if (newSelectedControls.length === selectedControls.length)
      newSelectedControls.push(control);
    setSelectedControls(newSelectedControls);
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
            disabled={selectedControls.length <= 0}
          >
            Изменить
          </button>
          <button
            className="disease-history__tool-bar-btn"
            disabled={selectedControls.length <= 0}
          >
            Удалить
          </button>
        </div>
      </div>

      <ul className="disease-history__timeline">
        {controls.map((control) => (
          <Control
            {...control}
            toggleSelect={() => toggleControlSelect(control)}
            key={control.id}
          />
        ))}
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
