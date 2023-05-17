import { useState } from "react";

import "./History.scss";

import ControlsTab from "./Tabs/ControlsTab";
import RubricsTab from "./Tabs/RubricsTab";

function History() {
  const [activeTab, setActiveTab] = useState("controls");

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
        {activeTab === "controls" ? <ControlsTab /> : <RubricsTab />}
      </div>
    </section>
  );
}

export default History;
