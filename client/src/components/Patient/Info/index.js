import { useEffect, useRef, useState } from "react";

import "./index.scss";

import { PATIENTS_URLS } from "../../../api/endpoints";
import usePatientId from "../../../hooks/usePatientId";
import useAuthorizedAxios from "../../../hooks/useAuthorizedAxios";
import useDebounce from "../../../hooks/useDebounce";

import LoadingSpinner from "../../UI/Spinner";

function Info() {
  const [patient, setPatient] = useState(null);

  const [isSaved, setIsSaved] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { patientId } = usePatientId();
  const authorizedAxios = useAuthorizedAxios();

  const unsavedChages = useRef({});

  const debouncedPatientUpdate = useDebounce(async () => {
    await authorizedAxios.patch(
      `${PATIENTS_URLS.PATIENT}?patient_id=${patientId}`,
      JSON.stringify(unsavedChages.current)
    );
    unsavedChages.current = {};
    setIsSaved(true);
  }, 1500);

  const onPatientPropChange = (e) => {
    const propName = e.target.id;
    const propValue = e.target.value;
    unsavedChages.current[propName] = propValue;
    setIsSaved(false);
    setPatient((patient) => ({ ...patient, [propName]: propValue }));
    debouncedPatientUpdate();
  };
  useEffect(() => {
    setIsLoading(true);
    const getPatient = async () => {
      const response = await authorizedAxios.get(
        `${PATIENTS_URLS.PATIENT}?patient_id=${patientId}`
      );
      setPatient(response.data);
      setIsLoading(false);
    };
    getPatient();
    // eslint-disable-next-line
  }, [patientId]);
  return (
    <section className="disease-info">
      {isLoading || !patient ? (
        <div className="disease-info__loading">
          <LoadingSpinner />
        </div>
      ) : (
        <div className="container">
          <div className="disease-info__row">
            <div className="disease-info__field">
              <label className="label" htmlFor="full_name">
                Фамилия и имя
              </label>
              <input
                className="input"
                type="text"
                id="full_name"
                value={patient.full_name || ""}
                onChange={onPatientPropChange}
              />
            </div>
            <div className="disease-info__field disease-info__field_small">
              <label className="label" htmlFor="age">
                Возраст
              </label>
              <input
                className="input"
                type="number"
                id="age"
                value={patient.age}
                onChange={onPatientPropChange}
              />
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
                value={patient.diagnosis || ""}
                onChange={onPatientPropChange}
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
                value={patient.complaints || ""}
                onChange={onPatientPropChange}
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
                value={patient.anamnesis || ""}
                onChange={onPatientPropChange}
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
                value={patient.heredity || ""}
                onChange={onPatientPropChange}
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
                value={patient.treatment_plan || ""}
                onChange={onPatientPropChange}
              ></textarea>
            </div>
          </div>
          <div className="disease-info__row">
            <div className="disease-info__field">
              <label className="label" htmlFor="treatment_comments">
                Комментарии
              </label>
              <textarea
                className="textarea"
                type="text"
                id="treatment_comments"
                rows="2"
                value={patient.treatment_comments || ""}
                onChange={onPatientPropChange}
              ></textarea>
            </div>
          </div>
          {isSaved && (
            <div className="disease-info__status-msg">Изменения сохранены</div>
          )}
        </div>
      )}
    </section>
  );
}

export default Info;
