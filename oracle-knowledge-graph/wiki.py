import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def scrape_quotes_to_excel():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = "http://quotes.toscrape.com/"
        print(f"Connecting to: {url}")
        
        try:
            await page.goto(url, wait_until="domcontentloaded")

            # Locate all quote containers on the page
            quote_elements = page.locator(".quote")
            count = await quote_elements.count()
            
            quotes_list = []

            # Loop through the first 10 quotes
            for i in range(min(10, count)):
                container = quote_elements.nth(i)
                
                text = await container.locator(".text").inner_text()
                author = await container.locator(".author").inner_text()
                tags = await container.locator(".tags").inner_text()

                quotes_list.append({
                    "Quote": text.strip("“”"),
                    "Author": author,
                    "Tags": tags.replace("Tags:", "").strip()
                })

            # Create Excel file
            df = pd.DataFrame(quotes_list)
            filename = "Top_10_Quotes.xlsx"
            df.to_excel(filename, index=False)
            
            print(f"✅ Success! Created {filename} with {len(df)} rows.")
            print(df.head(3)) # Show a preview in terminal

        except Exception as e:
            print(f"❌ Error: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_quotes_to_excel())