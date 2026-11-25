import asyncio
from playwright.async_api import async_playwright

SETTLE = "document.fonts.ready.then(() => [...document.images].every(i => i.complete))"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--hide-scrollbars"])
        for scheme in ("dark", "light"):
            for h in (720, 900):
                ctx = await b.new_context(viewport={"width": 1280, "height": h}, device_scale_factor=2, color_scheme=scheme)
                pg = await ctx.new_page()
                await pg.goto("http://localhost:8000/", wait_until="networkidle")
                await pg.wait_for_selector(".comp img.cv")
                await pg.wait_for_function(SETTLE)
                await pg.wait_for_timeout(1500)
                print(scheme, h, "Archivo loaded:", await pg.evaluate("document.fonts.check('800 40px Archivo')"))
                await pg.screenshot(path=f"shots/calendar-{scheme}-{h}.png")
                if h == 900:
                    await pg.click(".comp")
                    await pg.wait_for_timeout(2500)
                    await pg.screenshot(path=f"shots/midyears-{scheme}.png")
                await ctx.close()
        await b.close()

asyncio.run(main())
