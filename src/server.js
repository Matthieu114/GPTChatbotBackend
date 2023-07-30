const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const MessageModel = require('./models/Message');

const app = express();
app.use(cors());
app.use(express.json());

let chatMessages = [];

app.post('/api/process-prompt', async (req, res) => {
  try {
    let result = '';
    const { message } = req.body;

    // add user message to chat history
    chatMessages.push(new MessageModel(message.text, message.sender));
    const python = spawn('python', ['chatbot.py', message.text]);

    const promise = new Promise((resolve, reject) => {
      python.stdout.on('data', function (gptPrompt) {
        result += gptPrompt.toString();
      });

      python.on('close', (code) => {
        resolve();
      });

      python.on('error', (error) => {
        reject(error);
      });
    });

    await promise;

    chatMessages.push(new MessageModel(JSON.parse(result), 'chatGpt'));

    res.status(200);
    res.json(chatMessages);
  } catch (error) {
    res.status(400);
    res.json({ error: true, msg: error });
  }
});

app.get('/api/chat-messages', (req, res) => {
  res.json(chatMessages);
});

const port = 4000;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
