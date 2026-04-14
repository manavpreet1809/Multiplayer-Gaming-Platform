const puppeteer = require('puppeteer');
const path = require('path');

const SCREENS = [
  { id: 'ss-login', name: '01-login' },
  { id: 'ss-register', name: '02-register' },
  { id: 'ss-reset-password', name: '03-reset-password' },
  { id: 'ss-dashboard', name: '04-dashboard' },
  { id: 'ss-dashboard-ready', name: '05-dashboard-game-ready' },
  { id: 'ss-game-list', name: '06-game-list' },
  { id: 'ss-game-lobby', name: '07-game-lobby' },
  { id: 'ss-chat', name: '08-chat' },
  { id: 'ss-profile', name: '09-profile' },
  { id: 'ss-leaderboard', name: '10-leaderboard' },
  { id: 'ss-results-win', name: '11-game-results-win' },
  { id: 'ss-results-loss', name: '12-game-results-loss' },
  { id: 'ss-results-draw', name: '13-game-results-draw' },
  { id: 'ss-tictactoe', name: '14-tictactoe-board' },
  { id: 'ss-tictactoe-win', name: '15-tictactoe-win' },
  { id: 'ss-chess', name: '16-chess-board-white' },
  { id: 'ss-chess-black', name: '17-chess-board-black' },
];

const PORT = process.env.PORT || 3000;
const URL = `http://localhost:${PORT}/?screenshots`;
const OUT_DIR = path.join(__dirname, 'screenshots');

async function capture() {
  console.log(`Opening ${URL} ...\n`);

  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });

  await page.goto(URL, { waitUntil: 'networkidle0', timeout: 30000 });

  // Wait for fonts to load
  await page.evaluate(() => document.fonts.ready);

  for (const { id, name } of SCREENS) {
    const el = await page.$(`#${id}`);
    if (!el) {
      console.log(`  SKIP  ${name} (#${id} not found)`);
      continue;
    }
    const file = path.join(OUT_DIR, `${name}.png`);
    await el.screenshot({ path: file });
    console.log(`  SAVED ${name}.png`);
  }

  await browser.close();
  console.log(`\nDone! ${SCREENS.length} screenshots saved to screenshots/`);
}

capture().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
