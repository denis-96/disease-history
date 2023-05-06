import "./Info.scss";

function Info() {
  return (
    <section className="disease-info">
      <div className="container">
        <div className="disease-info__row">
          <div className="disease-info__field">
            <label className="label" htmlFor="patient_name">
              Фамилия и имя
            </label>
            <input className="input" type="text" id="patient_name" />
          </div>
          <div className="disease-info__field disease-info__field_small">
            <label className="label" htmlFor="patient_age">
              Возраст
            </label>
            <input className="input" type="number" id="patient_age" />
          </div>
        </div>
        <div className="disease-info__row">
          <div className="disease-info__field">
            <label className="label" htmlFor="diagnosis">
              Диагноз
            </label>
            <textarea
              className="textarea"
              type="text"
              id="diagnosis"
              rows="2"
            ></textarea>
          </div>
        </div>
        <div className="disease-info__row">
          <div className="disease-info__field">
            <label className="label" htmlFor="complaints">
              Жалобы
            </label>
            <textarea
              className="textarea"
              type="text"
              id="complaints"
              rows="2"
            ></textarea>
          </div>
        </div>
        <div className="disease-info__row">
          <div className="disease-info__field">
            <label className="label" htmlFor="anamnesis">
              Анамнез
            </label>
            <textarea
              className="textarea"
              type="text"
              id="anamnesis"
              rows="2"
            ></textarea>
          </div>
        </div>
        <div className="disease-info__row">
          <div className="disease-info__field">
            <label className="label" htmlFor="heredity">
              Наследственность
            </label>
            <textarea
              className="textarea"
              type="text"
              id="heredity"
              rows="2"
            ></textarea>
          </div>
        </div>
        <div className="disease-info__row">
          <div className="disease-info__field">
            <label className="label" htmlFor="treatment_plan">
              План лечения
            </label>
            <textarea
              className="textarea"
              type="text"
              id="treatment_plan"
              rows="2"
            ></textarea>
          </div>
        </div>
        <div className="disease-info__row">
          <div className="disease-info__field">
            <label className="label" htmlFor="comments">
              Комментарии
            </label>
            <textarea
              className="textarea"
              type="text"
              id="comments"
              rows="2"
            ></textarea>
          </div>
        </div>
        <div className="disease-info__status-msg">Изменения сохранены</div>
      </div>
    </section>
  );
}

export default Info;
