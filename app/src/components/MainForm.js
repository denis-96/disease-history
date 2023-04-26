import { Form, Row, Col } from "react-bootstrap";
import Input from "./UI/Input";
import Label from "./UI/Label";
import TextArea from "./UI/TextArea";

function MainForm() {
  return (
    <>
      <Label htmlFor="name">Фамилия и имя</Label>
      <Input type="text" name="name" />
      <Label htmlFor="name">Фамилия и имя</Label>
      <TextArea type="text" name="name" rows={2} />
      <Form>
        <Row className="mb-3">
          <Form.Group as={Col} controlId="exampleForm.ControlInput1">
            <Form.Label>Фамилия и имя</Form.Label>
            <Form.Control type="text" />
          </Form.Group>
          <Form.Group as={Col} xs={2} controlId="exampleForm.ControlInput1">
            <Form.Label>Возраст</Form.Label>
            <Form.Control type="number" />
          </Form.Group>
        </Row>
        <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
          <Form.Label>Диагноз</Form.Label>
          <Form.Control as="textarea" rows={2} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
          <Form.Label>Жалобы</Form.Label>
          <Form.Control as="textarea" rows={2} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
          <Form.Label>Анамнез</Form.Label>
          <Form.Control as="textarea" rows={2} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
          <Form.Label>Наследственность</Form.Label>
          <Form.Control as="textarea" rows={1} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
          <Form.Label>План лечения</Form.Label>
          <Form.Control as="textarea" rows={2} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
          <Form.Label>Комментарии</Form.Label>
          <Form.Control as="textarea" rows={2} />
        </Form.Group>
      </Form>
    </>
  );
}

export default MainForm;
