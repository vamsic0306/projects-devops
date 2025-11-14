import { useState, useEffect } from "react";
import API from "../api";

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [form, setForm] = useState({ product: "", amount: "" });

  async function load() {
    const res = await API.get("/orders/orders");
    setOrders(res.data.orders || []);
  }

  async function create(e) {
    e.preventDefault();
    await API.post("/orders/orders", form);
    load();
  }

  useEffect(() => { load(); }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Your Orders</h2>

      <form onSubmit={create}>
        <input placeholder="Product" onChange={(e)=>setForm({...form, product:e.target.value})} /><br/>
        <input placeholder="Amount" onChange={(e)=>setForm({...form, amount:e.target.value})} /><br/>
        <button type="submit">Create Order</button>
      </form>

      <h3>Order History</h3>
      <ul>
        {orders.map(o => (
          <li key={o.id}>
            #{o.id} - {o.product} - ${o.amount}
          </li>
        ))}
      </ul>
    </div>
  );
}
