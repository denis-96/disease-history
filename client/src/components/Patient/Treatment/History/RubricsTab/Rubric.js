import "./Rubric.scss";

function Rubric({ controlDate, controlTitle, rubricDescr }) {
  return (
    <li className="rubric-record">
      <div className="rubric-record__date">
        {new Date(controlDate + "Z").toString()}
      </div>
      <div className="rubric-record__control-title">{controlTitle}</div>
      <div className="rubric-record__content">{rubricDescr}</div>
    </li>
  );
}

export default Rubric;
