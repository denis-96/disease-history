import "./Record.css";

import { Accordion, Form } from "react-bootstrap";

function Record() {
  return (
    <div className="record">
      <div className="date">12.04.23</div>
      <Accordion>
        <Accordion.Item eventKey="0">
          <Accordion.Header>
            <Form.Check className="me-3 mb-1" type="checkbox" />
            Целенаправленный опрос
          </Accordion.Header>
          <Accordion.Body>
            <div className="mb-3">
              <Form.Group controlId="exampleForm.ControlInput1">
                <Form.Label>1. Cras justo odio</Form.Label>
                <Form.Control
                  as="textarea"
                  rows="auto"
                  type="text"
                  readOnly
                  value="Some quick example text to build on the card title and make up the bulk of the card's content.
                  Some quick example text to build on the card title and make up the bulk of the card's content.
                  Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to build on the card title and make up the bulk of the card's content."
                />
              </Form.Group>
            </div>

            <div className="mb-3">
              <Form.Group controlId="exampleForm.ControlInput1">
                <Form.Label>2. Cras justo odio</Form.Label>
                <Form.Control
                  as="textarea"
                  type="text"
                  readOnly
                  value="Some quick example text to build on the card title and make up the bulk of the card's content."
                />
              </Form.Group>
            </div>
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    </div>
  );
}

export default Record;
