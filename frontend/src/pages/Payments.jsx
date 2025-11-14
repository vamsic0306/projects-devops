import { useState, useEffect } from "react";
import API from "../api";

export default function Payments() {
  const [payments, setPayments] = useState([]);
  const [orderId, setOrderId] = useState("");
  const [amount, setAmount] = useState("");

  async function load() {
    const res = await API.get("/payments/payments");
    setPayments(res.data.payments || []);
  }

  async function pay(e) {
    e.preventDefault();
    await API.post("/payments/pay", { order_id: Number(orderId), amount });
    load();
  }

  useEffect(() => { load(); }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Payments</h2>

      <form onSubmit={pay}>
        <input placeholder="Order ID" onChange={(e)=>setOrderId(e.target.value)} /><br/>
        <input placeholder="Amount" onChange={(e)=>setAmount(e.target.value)} /><br/>
        <button type="submit">Pay</button>
      </form>

      <h3>Your Payments</h3>
      <ul>
        {payments.map(p => (
          <li key={p.id}>
            Payment #{p.id} — Order #{p.order_id} — ${p.amount}
          </li>
        ))}
      </ul>
    </div>
  );
}
