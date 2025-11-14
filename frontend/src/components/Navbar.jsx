import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const nav = useNavigate();

  function logout() {
    localStorage.removeItem("token");
    nav("/login");
  }

  return (
    <nav style={{ padding: 20, background: "#eee" }}>
      <Link to="/dashboard">Home</Link> |{" "}
      <Link to="/orders">Orders</Link> |{" "}
      <Link to="/payments">Payments</Link> |{" "}
      <button onClick={logout}>Logout</button>
    </nav>
  );
}
