import { ButtonGroup, Button } from "react-bootstrap";

import "./TimeLine.css";

import Record from "./Record";

function TimeLine() {
  return (
    <>
      <ButtonGroup>
        <Button>Left</Button>
        <Button>Middle</Button>
        <Button>Right</Button>
      </ButtonGroup>
      <ul class="time-line">
        <li>
          <Record />
        </li>
        <li>
          <Record />
        </li>
        <li>
          <Record />
        </li>
      </ul>
    </>
  );
}

export default TimeLine;
