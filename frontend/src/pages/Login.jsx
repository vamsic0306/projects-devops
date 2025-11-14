import { useState } from "react";
import API from "../api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const nav = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [msg, setMsg] = useState("");

  async function submit(e) {
    e.preventDefault();
    try {
      const res = await API.post("/users/login", form);
      localStorage.setItem("token", res.data.token);
      nav("/dashboard");
    } catch {
      setMsg("Invalid email or password");
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <input placeholder="Email" onChange={(e)=>setForm({...form, email:e.target.value})} /><br/>
        <input type="password" placeholder="Password" onChange={(e)=>setForm({...form, password:e.target.value})} /><br/>
        <button type="submit">Login</button>
      </form>
      <p>{msg}</p>
    </div>
  );
}
