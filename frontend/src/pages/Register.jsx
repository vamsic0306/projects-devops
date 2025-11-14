import { useState } from "react";
import API from "../api";

export default function Register() {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [msg, setMsg] = useState("");

  async function submit(e) {
    e.preventDefault();
    try {
      await API.post("/users/register", form);
      setMsg("Registered! You can login now.");
    } catch {
      setMsg("Error: Email already exists");
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Register</h2>
      <form onSubmit={submit}>
        <input placeholder="Name" onChange={(e)=>setForm({...form, name:e.target.value})} /><br/>
        <input placeholder="Email" onChange={(e)=>setForm({...form, email:e.target.value})} /><br/>
        <input type="password" placeholder="Password" onChange={(e)=>setForm({...form, password:e.target.value})} /><br/>
        <button type="submit">Register</button>
      </form>
      <p>{msg}</p>
    </div>
  );
}
