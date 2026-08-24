/*const axios = require("axios");

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
checkSite();/*
const axios = require("axios");

const BOT_TOKEN = "8736978159:AAHXzdOoAE4O_F6n0229xgNNmpiBJ78vRCI";
const CHAT_ID = "6868121119";

const URL = "https://karurcinemas.com";
const KEYWORDS = ["toxic", "sons", "kattu", "and"];

async function checkSite() {
  try {
    console.log("Checking site...");

    const res = await axios.get(URL);
    const text = res.data.toLowerCase();

    KEYWORDS.forEach(keyword => {
      if (text.includes(keyword)) {
        console.log("Found:", keyword);

        sendTelegram(`🎬 Movie Found: ${keyword}`);
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
*/
const axios = require("axios");

const BOT_TOKEN = "8736978159:AAHXzdOoAE4O_F6n0229xgNNmpiBJ78vRCI";
const CHAT_ID = "6868121119";

const URL = "https://karurcinemas.com";

// Toxic related keywords
const KEYWORDS = [
  "toxic",
  "toxic movie",
  "Irumudi",
  "kgf star toxic"
];

let lastFoundTime = null;   // when last keyword found
let lastNotified = 0;       // prevent spam for "not yet received"

async function checkSite() {
  try {
    console.log("Checking site...");

    const res = await axios.get(URL);
    const text = res.data.toLowerCase();

    let found = false;

    KEYWORDS.forEach(keyword => {
      if (text.includes(keyword)) {
        found = true;
      }
    });

    const now = Date.now();

    if (found) {
      console.log("Toxic movie FOUND");

      lastFoundTime = now;

      sendTelegram("🎬 Toxic movie started booking display 🔥");

    } else {
      console.log("Not found");

      // If not found for 15 minutes
      if (
        (!lastFoundTime || now - lastFoundTime > 15 * 60 * 1000) &&
        (now - lastNotified > 15 * 60 * 1000)
      ) {
        sendTelegram("⏳ Akash 9");
        lastNotified = now;
      }
    }

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

// Run every 60 sec
setInterval(checkSite, 60000);

// Run immediately
checkSite();
/*const axios = require("axios");

const BOT_TOKEN = "8736978159:AAHXzdOoAE4O_F6n0229xgNNmpiBJ78vRCI";
const CHAT_ID = "6868121119";

const URL = "https://karurcinemas.com";
let KEYWORDS = ["toxic", "karuppu", "kattu"];

let lastFoundTime = 0;
let sending = true;

function delay(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function checkSite() {
  try {
    console.log("Checking site...");

    const res = await axios.get(URL);
    const text = res.data.toLowerCase();

    let found = false;

    for (let keyword of KEYWORDS) {
      if (text.includes(keyword)) {
        found = true;

        console.log("Found:", keyword);

        if (sending) {
          await sendTelegram(`🎬 ${keyword} movie started booking! 🔥`);

          // 🔥 prevent spam
          await delay(3000);
        }

        lastFoundTime = Date.now();
      }
    }

    // ⏱️ If NOT found for 15 mins
    if (!found && Date.now() - lastFoundTime > 15 * 60 * 1000) {
      await sendTelegram("❌ Not yet received booking...");
      await delay(3000);
      lastFoundTime = Date.now();
    }

  } catch (err) {
    console.log("Error:", err.message);
  }
}

async function sendTelegram(msg) {
  try {
    await axios.post(
      `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`,
      {
        chat_id: CHAT_ID,
        text: msg
      }
    );
  } catch (err) {
    console.log("Telegram error:", err.message);
  }
}*/
