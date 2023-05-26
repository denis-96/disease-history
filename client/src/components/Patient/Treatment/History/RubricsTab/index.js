import { useEffect, useRef, useState } from "react";

import "./index.scss";

import RubricsSelect from "../../../../UI/RubricsSelect";
import Rubric from "./Rubric";

function RubricsTab({ controls }) {
  const [rubrics, setRubrics] = useState([]);
  const selectedRubric = useRef(null);

  const onRubricSelect = ({ rubricId }) => {
    selectedRubric.current = rubricId;
    const rubrics = controls.reduce((prev, { date, title, rubrics }) => {
      const rubric = rubrics.find((rubric) => +rubric.rubric.id === +rubricId);
      return rubric
        ? [
            ...prev,
            {
              controlTitle: title,
              controlDate: date,
              rubricDescr: rubric.description,
              id: rubric.id,
            },
          ]
        : prev;
    }, []);
    setRubrics(rubrics);
  };
  useEffect(
    () => onRubricSelect({ rubricId: selectedRubric.current }),
    // eslint-disable-next-line
    [controls]
  );

  return (
    <div className="disease-history__content">
      <div className="disease-history__rubric-selection">
        Выберите рубрику
        <RubricsSelect onSelect={onRubricSelect} />
      </div>
      <ul className="disease-history__timeline">
        {rubrics?.length ? (
          rubrics.map((rubric) => <Rubric key={rubric.id} {...rubric} />)
        ) : (
          <p className="disease-history__no-controls">Рубрик не найдено</p>
        )}
      </ul>
    </div>
  );
}

export default RubricsTab;
