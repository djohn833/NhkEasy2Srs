import * as fs from 'fs';
import * as puppeteer from 'puppeteer';

async function main() {
  const browser = await puppeteer.launch({
    // headless: false
  });

  const page = await browser.newPage();

  await page.goto('https://www3.nhk.or.jp/news/easy/');

  const archivesNext = (await page.$x('//*[@id="easy-wrapper"]/div[2]/aside/section[2]/div[1]/a[1]'))[0];
  const archivesPrev = (await page.$x('//*[@id="easy-wrapper"]/div[2]/aside/section[2]/div[1]/a[2]'))[0];

  // Start at the most recent news.
  await archivesNext.click();

  for (;;) {
    const archivesLinks = await page.$x('//*[@id="js-archives-list"]/a');

    for (const link of archivesLinks) {
      let hrefProp = await link.getProperty('href');
      const href = await hrefProp.jsonValue();
      console.log(href);
    }

    // Get as much older news as possible.
    const classProp = await archivesPrev.getProperty('className');
    const classValue = String(await classProp.jsonValue());
    if (classValue.includes("is-disabled")) {
      break;
    }

    await archivesPrev.click();
  }

  await browser.close();
}

main();