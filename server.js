const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());

app.post('/webhook', (req, res) => {
  const event = req.headers['x-github-event'];
  const payload = req.body;

  if (event === 'membership' && payload.action === 'added') {
    const member = payload.member.login;
    console.log(`🎉 Hello, @${member}! Welcome to ROFIES-IIITP GitHub organization!`);
    console.log("🤖 We're thrilled to have you on board.");
    console.log("🚀 Feel free to explore our projects and contribute your ideas.");
    console.log("🌟 If you have any questions or need assistance, don't hesitate to reach out!");
  }

  res.status(200).send('Webhook received');
});

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
