Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    document.getElementById('improve-btn').onclick = improveText;
  }
});

async function improveText() {
  try {
    const text = await getSelectedText();
    const improvedText = await sendToBackend(text);
    await replaceSelectedText(improvedText);
  } catch (error) {
    showError(error.message);
  }
}

async function getSelectedText() {
  return Word.run(async (context) => {
    const range = context.document.getSelection();
    range.load('text');
    await context.sync();
    return range.text;
  });
}

async function replaceSelectedText(text) {
  return Word.run(async (context) => {
    const range = context.document.getSelection();
    range.insertText(text, 'Replace');
    await context.sync();
  });
}

async function sendToBackend(text) {
  const response = await fetch('http://localhost:5000/improve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, action: 'rewrite' }),
  });
  const data = await response.json();
  return data.improvedText;
}

function showError(message) {
  document.getElementById('error-message').innerText = message;
}