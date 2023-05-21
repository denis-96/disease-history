import "./index.scss";

import useLocalStorage from "../../../../hooks/useLocalStorage";

import ControlsTab from "./ControlsTab";
import RubricsTab from "./RubricsTab";

function History({ controls, onUpdate }) {
  const [activeTab, setActiveTab] = useLocalStorage("activeTab", "controls");

  const getTabBtnClass = (tab) => {
    return `
    switch__btn ${activeTab === tab ? "switch__btn_active" : ""}
    `;
  };

  return (
    <section className="disease-history">
      <div className="container">
        <div className="switch">
          <button
            className={getTabBtnClass("controls")}
            onClick={() => setActiveTab("controls")}
          >
            Контроли
          </button>
          <button
            className={getTabBtnClass("rubrics")}
            onClick={() => setActiveTab("rubrics")}
          >
            Рубрики
          </button>
        </div>
        {activeTab === "controls" ? (
          <ControlsTab controls={controls} onUpdate={onUpdate} />
        ) : (
          <RubricsTab controls={controls} />
        )}
      </div>
    </section>
  );
}

export default History;
