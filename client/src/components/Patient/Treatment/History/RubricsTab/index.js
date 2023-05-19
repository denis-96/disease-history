import "./index.scss";

import RubricsSelect from "../../../../UI/RubricsSelect";
import Rubric from "./Rubric";

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
