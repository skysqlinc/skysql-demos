// Simple embeddable chat widget for SkySQL DB Agent
(function() {
  // Create chat icon
  const chatIcon = document.createElement('div');
  chatIcon.id = 'skysql-chat-icon';
  chatIcon.style.position = 'fixed';
  chatIcon.style.bottom = '24px';
  chatIcon.style.right = '24px';
  chatIcon.style.width = '64px';
  chatIcon.style.height = '64px';
  chatIcon.style.background = '#0072CE';
  chatIcon.style.borderRadius = '50%';
  chatIcon.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
  chatIcon.style.display = 'flex';
  chatIcon.style.alignItems = 'center';
  chatIcon.style.justifyContent = 'center';
  chatIcon.style.cursor = 'pointer';
  chatIcon.style.zIndex = '9999';
  chatIcon.innerHTML = '<img src="skysql_logo.png" alt="SkySQL" style="width:40px;height:40px;object-fit:contain;" />';
  document.body.appendChild(chatIcon);

  // Create chat window
  const chatWindow = document.createElement('div');
  chatWindow.id = 'skysql-chat-window';
  chatWindow.style.position = 'fixed';
  chatWindow.style.bottom = '100px';
  chatWindow.style.right = '24px';
  chatWindow.style.width = '420px';
  chatWindow.style.height = '600px';
  chatWindow.style.background = 'white';
  chatWindow.style.border = '1px solid #ccc';
  chatWindow.style.borderRadius = '12px';
  chatWindow.style.boxShadow = '0 4px 24px rgba(0,0,0,0.18)';
  chatWindow.style.display = 'none';
  chatWindow.style.flexDirection = 'column';
  chatWindow.style.zIndex = '10000';
  chatWindow.innerHTML = `
    <div style="background:#0072CE;color:white;padding:16px 20px;border-radius:12px 12px 0 0;font-weight:bold;font-size:1.2em;display:flex;align-items:center;gap:10px;">
      <img src="skysql_logo.png" alt="SkySQL" style="width:32px;height:32px;object-fit:contain;vertical-align:middle;" />
      SkySQL DB Chat
    </div>
    <div id="skysql-chat-messages" style="flex:1;overflow-y:auto;padding:16px;height:440px;"></div>
    <form id="skysql-chat-form" style="display:flex;padding:12px 16px 16px 16px;">
      <input id="skysql-chat-input" type="text" placeholder="Type your question..." style="flex:1;padding:10px;border-radius:6px;border:1px solid #ccc;font-size:1em;" />
      <button type="submit" style="margin-left:10px;background:#0072CE;color:white;border:none;border-radius:6px;padding:10px 20px;font-size:1em;">Send</button>
    </form>
  `;
  document.body.appendChild(chatWindow);

  // Show/hide chat window
  chatIcon.onclick = function() {
    chatWindow.style.display = chatWindow.style.display === 'none' ? 'flex' : 'none';
  };

  // Session management
  let sessionId = localStorage.getItem('skysql_chat_session_id');
  if (!sessionId) {
    sessionId = Math.random().toString(36).substr(2, 12) + Date.now();
    localStorage.setItem('skysql_chat_session_id', sessionId);
  }

  // Handle chat form submit
  const chatForm = chatWindow.querySelector('#skysql-chat-form');
  const chatInput = chatWindow.querySelector('#skysql-chat-input');
  const chatMessages = chatWindow.querySelector('#skysql-chat-messages');

  chatForm.onsubmit = async function(e) {
    e.preventDefault();
    const msg = chatInput.value.trim();
    if (!msg) return;
    appendMessage('user', msg);
    chatInput.value = '';
    appendMessage('agent', '<em>Thinking...</em>');
    const resp = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message: msg })
    });
    const data = await resp.json();
    // Remove 'Thinking...' placeholder
    removeLastAgentMessage();
    appendMessage('agent', data.response, data.sql);
  };

  function appendMessage(sender, text, sql) {
    const msgDiv = document.createElement('div');
    msgDiv.style.margin = '8px 0';
    msgDiv.style.textAlign = sender === 'user' ? 'right' : 'left';
    if (sender === 'agent') {
      // Render markdown using marked.js
      let html = window.marked ? window.marked.parse(text) : text;
      if (sql) {
        html += `<pre style="background:#f6f8fa;border-radius:6px;padding:12px;margin-top:8px;overflow-x:auto;"><code>${sql}</code></pre>`;
      }
      msgDiv.innerHTML = `<span style="background:#f4f4f4;padding:8px 12px;border-radius:8px;display:inline-block;max-width:80%;">${html}</span>`;
    } else {
      msgDiv.innerHTML = `<span style="background:#e6f0fa;padding:8px 12px;border-radius:8px;display:inline-block;max-width:80%;">${text}</span>`;
    }
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function removeLastAgentMessage() {
    const msgs = chatMessages.querySelectorAll('div');
    for (let i = msgs.length - 1; i >= 0; i--) {
      if (msgs[i].style.textAlign === 'left') {
        chatMessages.removeChild(msgs[i]);
        break;
      }
    }
  }
})(); 