import { useContext, useEffect, useState } from "react";

import "./Nav.scss";
import questionIcon from "../assets/question.svg";
import Help from "./Modals/Help";
import { PATIENTS } from "../apiEndpoints";
import { tokenContext } from "../App";

function Nav({ onPatientSelect }) {
  const [isHelpModalOpen, setIsHelpModalOpen] = useState(false);
  const [patients, setPatients] = useState(null);
  const { token } = useContext(tokenContext);

  useEffect(() => {
    (async () => {
      const response = await fetch(PATIENTS.ALL, {
        method: "GET",
        credentials: "include",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        const json = await response.json();
        setPatients(json);
      }
    })();
  }, [token]);

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
                    onClick={() => onPatientSelect(patient)}
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
