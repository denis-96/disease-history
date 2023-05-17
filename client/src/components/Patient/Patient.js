import Info from "./Info";
import NewRecord from "./NewRecord";
import History from "./History/History";

function Patient({ patient }) {
  return (
    <>
      {patient && (
        <>
          <Info patient={patient} />
          <History />
          <NewRecord />
        </>
      )}
    </>
  );
}

export default Patient;
