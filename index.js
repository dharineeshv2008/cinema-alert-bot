const axios = require("axios");

const BOT_TOKEN = "8736978159:AAHXzdOoAE4O_F6n0229xgNNmpiBJ78vRCI";
const CHAT_ID = "6868121119";

const URL = "https://karurcinemas.com";
const KEYWORDS = ["toxic", "sons","kattu","and"];

let sent = [];

async function checkSite() {
  try {
    console.log("Checking site...");

    const res = await axios.get(URL);
    const text = res.data.toLowerCase();

    KEYWORDS.forEach(keyword => {
      if (text.includes(keyword) && !sent.includes(keyword)) {
        console.log("Found:", keyword);

        sendTelegram(`🎬 Movie Found: ${keyword}`);
        sent.push(keyword);
      }
    });

  } catch (err) {
    console.log("Error:", err.message);
  }
}

function sendTelegram(msg) {
  axios.post(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
    chat_id: CHAT_ID,
    text: msg
  });
}

setInterval(checkSite, 60000);
checkSite();