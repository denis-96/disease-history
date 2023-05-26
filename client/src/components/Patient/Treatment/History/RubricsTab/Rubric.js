import "./Rubric.scss";

function Rubric({ controlDate, controlTitle, rubricDescr }) {
  return (
    <li className="rubric-record">
      <div className="rubric-record__date">
        {new Date(controlDate + "Z").toLocaleString("en-GB", {
          dateStyle: "short",
          timeStyle: "short",
          hour12: false,
        })}
      </div>
      <div className="rubric-record__control-title">{controlTitle}</div>
      <div className="rubric-record__content">{rubricDescr}</div>
    </li>
  );
}

export default Rubric;
