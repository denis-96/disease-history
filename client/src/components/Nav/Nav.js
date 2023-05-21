import { useEffect, useState } from "react";

import "./Nav.scss";

import { PATIENTS_URLS } from "../../api/endpoints";
import useAuthorizedAxios from "../../hooks/useAuthorizedAxios";

import Help from "../Modals/Help";
import usePatientId from "../../hooks/usePatientId";
import useLogout from "../../hooks/useLogout";

function Nav() {
  const [isHelpModalOpen, setIsHelpModalOpen] = useState(false);

  const [patients, setPatients] = useState(null);

  const { setPatientId } = usePatientId();
  const authorizedAxios = useAuthorizedAxios();
  const logout = useLogout();

  const createPatient = async () => {
    const response = await authorizedAxios.post(PATIENTS_URLS.PATIENT, "{}");
    setPatientId(response.data?.id);
  };

  useEffect(() => {
    const getPatients = async () => {
      const response = await authorizedAxios.get(PATIENTS_URLS.ALL);
      setPatients(response.data);
    };
    getPatients();
    // eslint-disable-next-line
  }, []);

  return (
    <nav className="nav">
      <div className="nav__container container">
        <div className="nav__links">
          <button className="nav__logout" onClick={logout}>
            Выход
          </button>
          <button
            className="nav__help"
            onClick={() => setIsHelpModalOpen(true)}
          >
            Помощь
          </button>
        </div>
        <div className="nav__dropdown">
          <button className="nav__dropdown-btn">Пациенты</button>
          <div className="nav__dropdown-content">
            <ul className="nav__dropdown-list">
              {patients?.length ? (
                patients.map((patient) => (
                  <li
                    key={patient.id}
                    onClick={() => {
                      setPatientId(patient.id);
                      localStorage.setItem("selectedPatientId", patient.id);
                    }}
                    className="nav__dropdown-item"
                  >
                    {patient.full_name}
                  </li>
                ))
              ) : (
                <p className="nav__dropdown-no-patients">Нет пациентов</p>
              )}
            </ul>
            <hr />
            <button
              className="nav__dropdown-item nav__dropdown-item_btn"
              onClick={createPatient}
            >
              Добавить
            </button>
          </div>
        </div>
      </div>

      {isHelpModalOpen && <Help onClose={() => setIsHelpModalOpen(false)} />}
    </nav>
  );
}

export default Nav;
