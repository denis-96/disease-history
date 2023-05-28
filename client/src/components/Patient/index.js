import "./index.scss";

import usePatientId from "../../hooks/usePatientId";

import Info from "./Info";
import Treatment from "./Treatment";

import { PATIENTS_URLS } from "../../api/endpoints";
import useAuthorizedAxios from "../../hooks/useAuthorizedAxios";

import deleteIcon from "../../assets/delete.svg";

function Patient() {
  const { patientId, setPatientId } = usePatientId();
  const authorizedAxios = useAuthorizedAxios();

  const deletePatient = async () => {
    if (window.confirm("Вы уверены, что хотите удалить пациента?")) {
      setPatientId(null);
      authorizedAxios.delete(PATIENTS_URLS.PATIENT, {
        params: { patient_id: patientId },
      });
    }
  };

  return patientId ? (
    <>
      <button
        className="patient__delete-btn"
        onClick={deletePatient}
        title="Удалить пациента"
      >
        <img src={deleteIcon} alt="delete patient" />
      </button>
      <Info />
      <Treatment />
    </>
  ) : (
    <div className="patient__choose-msg">Выберите пациента</div>
  );
}

export default Patient;
