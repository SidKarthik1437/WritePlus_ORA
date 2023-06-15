from playwright.sync_api import sync_playwright

def getSnapshot(link, id, type, keyword):
    with sync_playwright() as p:
        
        id = str(keyword)+"_"+str(type)+"_"+str(id)
        filename = "./ss/" + id + ".jpeg"
        print("taking snap")
        
        try:
            browser = p.chromium.launch(headless = True)
            page = browser.new_page()
            page.goto(link)
            # page.wait_for_timeout(180000)
            page.screenshot(path=filename)
            # page.close()
            browser.close()
            print("snap taken")

        
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
                print("Error occurred:", str(e))

    return filename