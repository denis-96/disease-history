import { useEffect, useState } from "react";

import "./Nav.scss";

import { PATIENTS_URLS } from "../../api/endpoints";
import useAuthorizedAxios from "../../hooks/useAuthorizedAxios";

import Help from "../Modals/Help";
import questionIcon from "../../assets/question.svg";
import usePatientId from "../../hooks/usePatientId";

function Nav() {
  const [isHelpModalOpen, setIsHelpModalOpen] = useState(false);

  const [patients, setPatients] = useState(null);

  const { setPatientId } = usePatientId();
  const authorizedAxios = useAuthorizedAxios();

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
        <button onClick={() => setIsHelpModalOpen(true)} className="nav__btn">
          <img src={questionIcon} alt="help" className="nav__btn-icon" />
        </button>
        <div className="nav__dropdown">
          <button className="nav__dropdown-btn">Пациенты</button>
          <div className="nav__dropdown-content">
            <ul className="nav__dropdown-list">
              {patients &&
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
                ))}
            </ul>
            <hr />
            <button className="nav__dropdown-item nav__dropdown-item_btn">
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
