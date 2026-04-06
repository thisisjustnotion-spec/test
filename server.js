// server.js
const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, { cors: { origin: "*" } });

app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <title>YOLO 실시간 화면</title>
      <style>
        body { font-family: Arial; text-align: center; background: #111; color: white; }
        img { max-width: 90%; margin-top: 20px; border: 3px solid #0f0; }
      </style>
    </head>
    <body>
      <h1>🔥 Python YOLO → Node.js 실시간 이미지</h1>
      <img id="yoloImg" src="" alt="YOLO 이미지 대기중...">
      <p id="status">대기중...</p>

      <script src="/socket.io/socket.io.js"></script>
      <script>
        const socket = io();
        socket.on('image', (data) => {
          const img = document.getElementById('yoloImg');
          const status = document.getElementById('status');
          
          img.src = 'data:image/jpeg;base64,' + data.image;
          status.textContent = '업데이트됨 (${new Date().toLocaleTimeString()})';
          console.log('이미지 수신 완료!');
        });

        socket.on('connect', () => {
          console.log('Python과 연결 성공!');
        });
      </script>
    </body>
    </html>
  `);
});

io.on('connection', (socket) => {
  console.log('✅ Python(인공지능) 연결됨!');
});

httpServer.listen(3000, () => {
  console.log('🚀 Node.js 서버 시작! → http://localhost:3000');
});
