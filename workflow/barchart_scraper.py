import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_barchart_top_100():
    url = "https://www.barchart.com/stocks/top-100-stocks"
    output_file = "top_100_stocks.csv"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Wait for the table to load
        await page.wait_for_selector("table.bc-table")

        # Extract table headers
        headers = await page.eval_on_selector_all(
            "table.bc-table thead tr th",
            "ths => ths.map(th => th.innerText.trim())"
        )

        # Extract table rows
        rows = await page.eval_on_selector_all(
            "table.bc-table tbody tr",
            """trs => trs.map(tr => 
                Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim())
            )"""
        )

        # Save to CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"✅ Data saved to {output_file}")
        await browser.close()

# Run the async function
if __name__ == "__main__":
    asyncio.run(scrape_barchart_top_100())
