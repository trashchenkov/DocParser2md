import argparse, asyncio
from urllib.parse import urlparse, urljoin
from pathlib import Path
from collections import deque

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from playwright.async_api import async_playwright

class DocParser:
    def __init__(self, base_url, out_dir):
        self.base = base_url.rstrip('/')
        self.out = Path(out_dir)
        self.visited = set()
        self.to_visit = deque([self.base])
        self.out.mkdir(parents=True, exist_ok=True)

    async def fetch(self, page, url):
        await page.goto(url, wait_until='networkidle')
        return await page.content()

    def extract_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            href = urljoin(self.base, a['href'].split('#')[0])
            if href.startswith(self.base):
                href = href.rstrip('/')
                links.add(href)
        return links

    def extract_main(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        sel = soup.select_one('.document, article, #main-content, #content')
        return str(sel if sel else soup.body)

    def html_to_md(self, html):
        return md(html, heading_style='ATX')

    def save(self, url, text):
        path = urlparse(url).path.strip('/')
        fname = path.replace('/', '_') or 'index'
        (self.out / f"{fname}.md").write_text(text, encoding='utf-8')
        print(f"→ {fname}.md")

    async def crawl(self):
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page()
            while self.to_visit:
                url = self.to_visit.popleft()
                if url in self.visited:
                    continue
                self.visited.add(url)

                html = await self.fetch(page, url)
                for l in self.extract_links(html):
                    if l not in self.visited:
                        self.to_visit.append(l)

                main = self.extract_main(html)
                txt = self.html_to_md(main)
                self.save(url, txt)

            await browser.close()

async def main():
    p = argparse.ArgumentParser()
    p.add_argument('--url', required=True)
    p.add_argument('--out-dir', default='docs_md')
    args = p.parse_args()

    parser = DocParser(args.url, args.out_dir)
    await parser.crawl()

if __name__ == '__main__':
    asyncio.run(main())
