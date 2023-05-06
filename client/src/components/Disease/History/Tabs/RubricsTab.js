import "./RubricsTab.scss";

import RubricsSelect from "../../RubricsSelect";
import Rubric from "../Records/Rubric";

function RubricsTab() {
  return (
    <div className="disease-history__content">
      <div className="disease-history__rubric-selection">
        Выберите рубрику
        <RubricsSelect />
      </div>
      <ul className="disease-history__timeline">
        <Rubric />
        <Rubric />
        <Rubric />
        <Rubric />
      </ul>
    </div>
  );
}

export default RubricsTab;
