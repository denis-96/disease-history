import "./ControlCompare.scss";

function ControlCompare({ firstControl, secondControl, onClose }) {
  const rubrics = [];
  const firstControlRubrics = firstControl.changedRubrics;
  const secondControlRubrics = secondControl.changedRubrics;
  const rubricsQty =
    firstControlRubrics.length > secondControlRubrics.length
      ? firstControlRubrics.length
      : secondControlRubrics.length;

  for (let i = 0; i < rubricsQty; i++) {
    const firstRubric = firstControlRubrics[i];
    const secondRubric = secondControlRubrics[i];
    rubrics.push(
      <div className="control-compare__rubric" key={i}>
        <div className="control-compare__rubric-title">
          {firstRubric ? firstRubric.title : secondRubric.title}
        </div>
        <div className="control-compare__rubric-body">
          <div className="control-compare__rubric-descr">
            {firstRubric && firstRubric.content}
          </div>
          <div className="control-compare__rubric-descr">
            {secondRubric && secondRubric.content}
          </div>
        </div>
      </div>
    );
  }

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
        <div className="control-compare__rubrics">{rubrics}</div>
      </div>
    </div>
  );
}

export default ControlCompare;
