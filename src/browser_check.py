"""Run with an environment containing Playwright + Chromium; app must be on port 8000."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence/screenshots';OUT.mkdir(parents=True,exist_ok=True)
checks=[]
with sync_playwright() as p:
    chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    browser=p.chromium.launch(headless=True,executable_path=str(chrome) if chrome.exists() else None)
    context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1)
    page=context.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:8000/',wait_until='networkidle')
    page.wait_for_function("document.querySelector('#status').textContent.includes('kết quả')")
    assert 'Christopher Nolan' in page.locator('#results').inner_text()
    page.screenshot(path=str(OUT/'01_app.png'),full_page=False)
    checks.append({'check':'local endpoint UI, Inception','passed':True})
    page.select_option('#sample','2')
    page.wait_for_function("!document.querySelector('#run').disabled")
    assert page.locator('#results tbody tr').count()>=5
    page.screenshot(path=str(OUT/'02_nolan.png'),full_page=False)
    checks.append({'check':'Nolan query through endpoint','passed':True})
    page.goto('http://127.0.0.1:8000/resource/film-Q25188',wait_until='networkidle')
    assert page.locator('h1').inner_text()=='Inception'
    page.screenshot(path=str(OUT/'03_resource.png'),full_page=False)
    checks.append({'check':'IRI HTML and linked-data navigation','passed':True})
    page.goto('http://127.0.0.1:8000/?browser',wait_until='networkidle')
    page.wait_for_function("!document.querySelector('#run').disabled",timeout=45000)
    assert 'Christopher Nolan' in page.locator('#results').inner_text(),page.locator('#status').inner_text()
    checks.append({'check':'browser Comunica SELECT','passed':True})
    page.select_option('#sample','5')
    page.wait_for_function("!document.querySelector('#run').disabled",timeout=45000)
    assert page.locator('#results tbody tr').count()>0,page.locator('#status').inner_text()
    checks.append({'check':'browser Comunica GROUP BY / COUNT','passed':True})
    page.select_option('#sample','7')
    page.wait_for_function("!document.querySelector('#run').disabled",timeout=45000)
    assert 'Đúng (true)' in page.locator('#results').inner_text(),page.locator('#status').inner_text()
    checks.append({'check':'browser Comunica ASK','passed':True})
    page.locator('#query-text').fill('CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 3')
    page.click('#run');page.wait_for_function("!document.querySelector('#run').disabled",timeout=45000)
    assert page.locator('#results pre').count()==1,page.locator('#status').inner_text()
    checks.append({'check':'browser Comunica CONSTRUCT','passed':True})
    page.set_viewport_size({'width':390,'height':844})
    page.goto('http://127.0.0.1:8000/',wait_until='networkidle')
    page.wait_for_function("!document.querySelector('#run').disabled")
    assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
    page.screenshot(path=str(OUT/'04_mobile.png'),full_page=True)
    checks.append({'check':'mobile 390px, no page overflow','passed':True})
    assert not errors,errors
    checks.append({'check':'no uncaught browser exceptions','passed':True})
    context.close();browser.close()
(ROOT/'evidence/browser_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False,indent=2))
