import "./Nav.scss";
import questionIcon from "../assets/question.svg";

function Nav() {
  return (
    <nav className="nav">
      <div className="nav__container container">
        <button className="nav__btn">
          <img src={questionIcon} alt="help" className="nav__btn-icon" />
        </button>
        <div className="nav__dropdown">
          <button className="nav__dropdown-btn">Пациенты</button>
          <div className="nav__dropdown-content">
            <ul className="nav__dropdown-list">
              <li className="nav__dropdown-item">Имя Фамилия</li>
              <li className="nav__dropdown-item">Пациент</li>
              <li className="nav__dropdown-item">Пациент</li>
            </ul>
            <hr />
            <button className="nav__dropdown-item nav__dropdown-item_btn">
              Добавить
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Nav;
