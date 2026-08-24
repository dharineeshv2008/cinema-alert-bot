const axios = require("axios");

const BOT_TOKEN = "8736978159:AAHXzdOoAE4O_F6n0229xgNNmpiBJ78vRCI";
const CHAT_ID = "6868121119";

const URL = "https://karurcinemas.com";
const KEYWORDS = ["toxic"];

let isFound = false;
let lastNotFoundTime = 0;

// 🔍 Check site every 1 minute
async function checkSite() {
  try {
    console.log("Checking site...");

    const res = await axios.get(URL);
    const text = res.data.toLowerCase();

    let foundNow = false;

    for (let keyword of KEYWORDS) {
      if (text.includes(keyword)) {
        foundNow = true;
        console.log("Found:", keyword);
      }
    }

    isFound = foundNow;

    // ❌ NOT FOUND → send once every 5 min
    if (!isFound) {
      const now = Date.now();

      if (now - lastNotFoundTime > 5 * 60 * 1000) {
        sendTelegram("❌ Movie Not Found");
        lastNotFoundTime = now;
        console.log("Sent NOT FOUND");
      }
    }

  } catch (err) {
    console.log("Error:", err.message);
  }
}

// 📲 Send Telegram
function sendTelegram(msg) {
  axios.post(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
    chat_id: CHAT_ID,
    text: msg
  }).catch(err => console.log("Telegram Error:", err.message));
}

// 🔥 Continuous sender (every 5 sec if found)
setInterval(() => {
  if (isFound) {
    sendTelegram("🎬 Movie Found: toxic");
    console.log("Sending FOUND message...");
  }
}, 5000);

// ⏱ Check site every 1 minute
setInterval(checkSite, 60000);

// First run
checkSite();