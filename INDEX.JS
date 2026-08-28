const axios = require("axios");

const BOT_TOKEN = "8960512301:AAGQKknYUr7VSqfuLCEOnc4OilzfBaG0gs0";

// ✅ ADD MULTIPLE USERS HERE
const CHAT_IDS = [
  "6868121119",   // you
  "8122701018"    // friend
];

const URL = "https://karurcinemas.com";
const KEYWORDS = ["toxic", "ram", "leela"];

let sent = [];

// 🔍 CHECK WEBSITE
async function checkSite() {
  try {
    console.log("Checking site...");

    const res = await axios.get(URL);
    const text = res.data.toLowerCase();

    KEYWORDS.forEach(keyword => {
      if (text.includes(keyword) && !sent.includes(keyword)) {
        console.log("Found:", keyword);

        sendTelegram(`🔥🎬 MOVIE FOUND: ${keyword.toUpperCase()} 🎬🔥`);
        sent.push(keyword);
      }
    });

  } catch (err) {
    console.log("Error:", err.message);
  }
}

// 📩 SEND TO ALL USERS
function sendTelegram(msg) {
  CHAT_IDS.forEach(chatId => {
    axios.post(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
      chat_id: chatId,
      text: msg
    }).catch(err => console.log("Send Error:", err.message));
  });
}

// ⏱ RUN EVERY 1 MIN
setInterval(checkSite, 60000);
checkSite();