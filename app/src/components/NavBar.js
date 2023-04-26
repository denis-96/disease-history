import { Button, Dropdown, DropdownButton } from "react-bootstrap";

function NavBar() {
  return (
    <nav className="m-3 justify-content-between">
      <Button variant="secondary">?</Button>
      <DropdownButton id="dropdown-basic-button" title="Пациенты">
        <Dropdown.Item>Пациент 1</Dropdown.Item>
        <Dropdown.Item>Пациент 2</Dropdown.Item>
        <Dropdown.Item>Пациент 3</Dropdown.Item>
        <Dropdown.Divider />
        <Dropdown.Item>Создать</Dropdown.Item>
      </DropdownButton>
    </nav>
  );
}

export default NavBar;
