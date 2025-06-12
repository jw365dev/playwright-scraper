import asyncio
import csv
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def scrape_barchart_top_100():
    try:
        url = "https://www.barchart.com/stocks/top-100-stocks"
        output_file = "top_100_stocks.csv"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)  # 60 seconds

            try:
                await page.wait_for_selector("table.bc-table", timeout=30000)  # 30 seconds
            except PlaywrightTimeoutError:
                print("❌ Table did not load in time. Saving page content for debugging.")
                html = await page.content()
                with open("debug_page.html", "w", encoding="utf-8") as f:
                    f.write(html)
                await browser.close()
                return

            headers = await page.eval_on_selector_all(
                "table.bc-table thead tr th",
                "ths => ths.map(th => th.innerText.trim())"
            )

            rows = await page.eval_on_selector_all(
                "table.bc-table tbody tr",
                """trs => trs.map(tr => 
                    Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim())
                )"""
            )

            with open(output_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)

            print(f"✅ Data saved to {output_file}")
            await browser.close()

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(scrape_barchart_top_100())
