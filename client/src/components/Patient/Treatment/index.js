import { useState, useEffect } from "react";
import "./index.scss";

import { RECORDS_URLS } from "../../../api/endpoints";
import usePatientId from "../../../hooks/usePatientId";
import useAuthorizedAxios from "../../../hooks/useAuthorizedAxios";

import History from "./History";
import NewRecord from "./NewRecord";

function Treatment() {
  const [controls, setControls] = useState([]);

  const { patientId } = usePatientId();
  const authorizedAxios = useAuthorizedAxios();

  const getRecords = async () => {
    const response = await authorizedAxios.get(
      `${RECORDS_URLS.ALL}?patient_id=${patientId}`
    );
    setControls(response.data);
  };

  useEffect(() => {
    getRecords();
    // eslint-disable-next-line
  }, [patientId]);

  return (
    <>
      <History controls={controls} />
      <NewRecord onSubmit={getRecords} />
    </>
  );
}

export default Treatment;
