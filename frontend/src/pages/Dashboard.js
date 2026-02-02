import { useEffect, useState } from "react";
import api from "../api/axios";
import Navbar from "../components/Navbar";

export default function Dashboard() {
  const [profile, setProfile] = useState({});
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    api.get("/profile").then(res => setProfile(res.data));
    api.get("/tasks").then(res => setTasks(res.data));
  }, []);

  const addTask = async () => {
    if (!title) return;
    const res = await api.post("/tasks", { title });
    setTasks([...tasks, res.data]);
    setTitle("");
  };

  const deleteTask = async (id) => {
    await api.delete(`/tasks/${id}`);
    setTasks(tasks.filter(t => t.id !== id));
  };

  const filteredTasks = tasks.filter(
    t => t.title && t.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <Navbar />

      <div className="max-w-2xl mx-auto mt-8 bg-white p-6 rounded shadow">
        <h3 className="text-lg font-semibold mb-4">
          Welcome, {profile.email}
        </h3>

        <input
          className="w-full border p-2 mb-4 rounded"
          placeholder="Search tasks..."
          onChange={(e) => setSearch(e.target.value)}
        />

        <div className="flex mb-4">
          <input
            className="flex-1 border p-2 rounded-l"
            placeholder="New task"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <button
            onClick={addTask}
            className="bg-blue-600 text-white px-4 rounded-r hover:bg-blue-700"
          >
            Add
          </button>
        </div>

        <ul>
          {filteredTasks.map(t => (
            <li
              key={t.id}
              className="flex justify-between items-center border-b py-2"
            >
              <span>{t.title}</span>
              <button
                onClick={() => deleteTask(t.id)}
                className="text-red-500 hover:text-red-700"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
