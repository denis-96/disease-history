import "./Help.scss";

function Help({ onClose }) {
  return (
    <div
      onClick={(e) => e.target.matches(".overlay") && onClose()}
      className="overlay"
    >
      <div className="help container">
        <div className="help__head">
          Советы по созданию контролей
          <button onClick={onClose} className="help__close-btn">
            &#10006;
          </button>
        </div>
        <div className="help__content"></div>
        <hr />
        <div className="help__recomendation">
          <div className="help__recomendation-title">
            КОНТРОЛЬ № 1 ПО ПЕРВИЧНОЙ РЕАКЦИИ
          </div>
          <div className="help__recomendation-descr">
            Cимптомы первичной реакции первого дня, которых нет во второй день,
            справа – через сколько дней они появились в жалобах «Дневника». По
            данному методу контроля делается вывод: препарат закончил действие
            такого-то числа.
          </div>
        </div>
        <div className="help__recomendation">
          <div className="help__recomendation-title">
            КОНТРОЛЬ № 2 ПО МИАЗМУ
          </div>
          <div className="help__recomendation-descr">
            Cимптомы первичной реакции первого дня, которых нет во втором дне
            какие симптомы какого миазма ожидать с какой рубрики. И из дневника
            на данную дату мы можем отследить, когда появились эти симптомы,
            через сколько дней. По данному методу контроля делается вывод:
            препарат закончил действие такого-то числа.
          </div>
        </div>
        <div className="help__recomendation">
          <div className="help__recomendation-title">
            КОНТРОЛЬ № 3 ПО ТРЕТЬЕЙ РУБРИКЕ
          </div>
          <div className="help__recomendation-descr">
            Симптомы первичной реакции 1-го дня с третьей рубрике были такие-то.
            В дневнике они появились такого-то числа. По данному методу контроля
            делается вывод: препарат закончил действие такого-то числа.
          </div>
        </div>
        <div className="help__recomendation">
          <div className="help__recomendation-title">
            КОНТРОЛЬ № 4 ПО РУБРИКЕ, КОТОРОЙ ТРОПЕН ПРЕПАРАТ
          </div>
          <div className="help__recomendation-descr">
            Выбираем нужную рубрику, справа появляются симптомы первичной
            реакции первого дня, которых нет во втором дне, и через сколько дней
            они появились
          </div>
        </div>
      </div>
    </div>
  );
}

export default Help;
