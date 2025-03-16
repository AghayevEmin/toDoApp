import express, { Request, Response } from 'express';
import cors from 'cors';

const app = express();
const port = 3001; // Different from frontend port (5173)

// Middleware
app.use(cors()); // Allow frontend to access backend
app.use(express.json()); // Parse JSON bodies

// In-memory storage for tasks
let tasks: string[] = [];

// GET /tasks - Retrieve all tasks
app.get('/tasks', (req: Request, res: Response) => {
  res.json(tasks);
});

// POST /tasks - Add a new task
app.post('/tasks', (req: Request, res: Response) => {
  const { task } = req.body;
  if (typeof task === 'string' && task.trim() !== '') {
    tasks.push(task);
    res.status(201).json({ message: 'Task added', tasks });
  } else {
    res.status(400).json({ error: 'Invalid task' });
  }
});

// DELETE /tasks/:index - Delete a task by index
app.delete('/tasks/:index', (req: Request, res: Response) => {
  const index = parseInt(req.params.index, 10);
  if (isNaN(index) || index < 0 || index >= tasks.length) {
    res.status(400).json({ error: 'Invalid index' });
  } else {
    tasks = tasks.filter((_, i) => i !== index);
    res.json({ message: 'Task deleted', tasks });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Backend server running at http://localhost:${port}`);
});