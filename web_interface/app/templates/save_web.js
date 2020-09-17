const puppeteer = require('puppeteer');

async function run() {
  const browser = await puppeteer.launch({
    args: [
      '--window-size=1920,1080',
    ],
  });
  const page = await browser.newPage();

  await page.goto("file:/Users/tranquanghuy/EGH455/docker-python-gunicorn-nginx/starter-kit/index.html");
  await page.setViewport({
    width: 1260,
    height: 960
  })
  await page.screenshot({ path: 'mainPage.png', fullPage: true });

  browser.close();
}

run();