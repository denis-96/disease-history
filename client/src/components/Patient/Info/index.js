import { useEffect, useRef, useState } from "react";

import "./index.scss";

import { PATIENTS_URLS } from "../../../api/endpoints";
import usePatientId from "../../../hooks/usePatientId";
import useAuthorizedAxios from "../../../hooks/useAuthorizedAxios";
import useDebounce from "../../../hooks/useDebounce";

import LoadingSpinner from "../../UI/Spinner";
import Input from "../../UI/Input";

function Info() {
  const [patient, setPatient] = useState(null);

  const [isSaved, setIsSaved] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { patientId, setPatientId } = usePatientId();
  const authorizedAxios = useAuthorizedAxios();

  const unsavedChages = useRef({});

  const debouncedPatientUpdate = useDebounce(async () => {
    const changedKeys = Object.keys(unsavedChages.current);
    if (
      changedKeys.includes("full_name") &&
      unsavedChages.current.full_name.length < 3
    ) {
      return;
    }
    if (changedKeys.includes("age") && unsavedChages.current.age < 0) {
      return;
    }

    const response = await authorizedAxios.patch(
      `${PATIENTS_URLS.PATIENT}?patient_id=${patientId}`,
      JSON.stringify(unsavedChages.current)
    );
    unsavedChages.current = {};
    setPatient(response.data);
    setIsSaved(true);
  }, 1500);

  const onPatientPropChange = (propName, propValue) => {
    unsavedChages.current[propName] = propValue;
    setIsSaved(false);
    debouncedPatientUpdate();
  };

  const validateName = (name) => {
    if (name.length < 3) {
      return {
        isValid: false,
        message: "Не меньше 3 символов",
      };
    }
    return { isValid: true };
  };

  const validateAge = (age) => {
    if (+age < 0) {
      return {
        isValid: false,
        message: "Только положительные числа",
      };
    }
    return { isValid: true };
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
    getPatient().catch((e) => {
      if (e.response.status === 404) {
        setPatientId(null);
      }
    });
    // eslint-disable-next-line
  }, [patientId]);
  return (
    <section className="disease-info">
      {isLoading || !patient ? (
        <LoadingSpinner />
      ) : (
        <div className="container">
          <div className="disease-info__row">
            <div className="disease-info__field">
              <label className="label" htmlFor="full_name">
                Фамилия и имя
              </label>
              <Input
                id="full_name"
                initialValue={patient.full_name || ""}
                onChange={(value) => onPatientPropChange("full_name", value)}
                onValidation={validateName}
              />
            </div>
            <div className="disease-info__field disease-info__field_small">
              <label className="label" htmlFor="age">
                Возраст
              </label>
              <Input
                type="number"
                id="age"
                initialValue={patient.age}
                onChange={(value) => onPatientPropChange("age", value)}
                onValidation={validateAge}
              />
            </div>
          </div>
          <div className="disease-info__row">
            <div className="disease-info__field">
              <label className="label" htmlFor="diagnosis">
                Диагноз
              </label>
              <Input
                id="diagnosis"
                initialValue={patient.diagnosis || ""}
                onChange={(value) => onPatientPropChange("diagnosis", value)}
                isTextarea
              ></Input>
            </div>
          </div>
          <div className="disease-info__row">
            <div className="disease-info__field">
              <label className="label" htmlFor="complaints">
                Жалобы
              </label>
              <Input
                id="complaints"
                initialValue={patient.complaints || ""}
                onChange={(value) => onPatientPropChange("complaints", value)}
                isTextarea
              ></Input>
            </div>
          </div>
          <div className="disease-info__row">
            <div className="disease-info__field">
              <label className="label" htmlFor="anamnesis">
                Анамнез
              </label>
              <Input
                id="anamnesis"
                initialValue={patient.anamnesis || ""}
                onChange={(value) => onPatientPropChange("anamnesis", value)}
                isTextarea
              ></Input>
            </div>
          </div>
          <div className="disease-info__row">
            <div className="disease-info__field">
              <label className="label" htmlFor="heredity">
                Наследственность
              </label>
              <Input
                id="heredity"
                initialValue={patient.heredity || ""}
                onChange={(value) => onPatientPropChange("heredity", value)}
                isTextarea
              ></Input>
            </div>
          </div>
          <div className="disease-info__row">
            <div className="disease-info__field">
              <label className="label" htmlFor="treatment_plan">
                План лечения
              </label>
              <Input
                id="treatment_plan"
                initialValue={patient.treatment_plan || ""}
                onChange={(value) =>
                  onPatientPropChange("treatment_plan", value)
                }
                isTextarea
              ></Input>
            </div>
          </div>
          <div className="disease-info__row">
            <div className="disease-info__field">
              <label className="label" htmlFor="treatment_comments">
                Комментарии
              </label>
              <Input
                id="treatment_comments"
                initialValue={patient.treatment_comments || ""}
                onChange={(value) =>
                  onPatientPropChange("treatment_comments", value)
                }
                isTextarea
              ></Input>
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
