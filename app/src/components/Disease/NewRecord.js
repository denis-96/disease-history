import "./NewRecord.scss";

import RubricsSelect from "./RubricsSelect";

function NewRecord() {
  return (
    <section className="new-record">
      <div className="container">
        <div className="new-record__header">Добавить контроль</div>
        <input
          className="input new-record__title"
          type="text"
          placeholder="Название"
        />
        <div className="new-record__subheader">Изменившиеся рубрики:</div>
        <div className="new-record__rubric">
          <RubricsSelect />
          <textarea
            className="textarea new-record__rubric-descr"
            type="text"
            rows="1"
            placeholder="Опишите изменения"
          ></textarea>
        </div>
        <button className="new-record__add-rubric-btn">+</button>
        <button className="new-record__save-btn">Сохранить</button>
      </div>
    </section>
  );
}

export default NewRecord;
