import "./ControlCompare.scss";

function ControlCompare({ firstControl, secondControl, onClose }) {
  const firstControlRubrics = firstControl.rubrics;
  const secondControlRubrics = secondControl.rubrics;

  const rubrics = {};
  const transformControlRubrics = (controlKey, controlRubrics) => {
    controlRubrics.forEach((rubric) => {
      const rubricId = rubric.rubric.id;
      const rubricData = {
        rubricTitle: rubric.rubric.title,
        [controlKey]: rubric.description,
      };
      rubrics[rubricId] = rubrics[rubricId]
        ? { ...rubrics[rubricId], ...rubricData }
        : rubricData;
    });
  };
  transformControlRubrics("first", firstControlRubrics);
  transformControlRubrics("second", secondControlRubrics);

  const rubricsJsx = Object.entries(rubrics).map((rubric) => (
    <div className="control-compare__rubric" key={rubric[0]}>
      <div className="control-compare__rubric-title">
        {rubric[1].rubricTitle}
      </div>
      <div className="control-compare__rubric-body">
        <div className="control-compare__rubric-descr">{rubric[1].first}</div>
        <div className="control-compare__rubric-descr">{rubric[1].second}</div>
      </div>
    </div>
  ));

  return (
    <div
      onClick={(e) => e.target.matches(".overlay") && onClose()}
      className="overlay"
    >
      <div className="control-compare container">
        <div className="control-compare__head">
          Сравнение
          <button onClick={onClose} className="control-compare__close-btn">
            &#10006;
          </button>
        </div>
        <hr />
        <div className="control-compare__control-titles">
          <div className="control-compare__control-title">
            {firstControl.title}
          </div>
          <div className="control-compare__control-title">
            {secondControl.title}
          </div>
        </div>
        <div className="control-compare__rubrics">{rubricsJsx}</div>
      </div>
    </div>
  );
}

export default ControlCompare;
