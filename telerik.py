import urllib3
import requests
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate'}

def scan(url):
    paths = ["/DesktopModules/Admin/RadEditorProvider/DialogHandler.aspx","/app_master/telerik.web.ui.dialoghandler.aspx","/Providers/HtmlEditorProviders/Telerik/Telerik.Web.UI.DialogHandler.aspx",
    "/common/admin/Jobs2/Telerik.Web.UI.DialogHandler.aspx","/dashboard/UserControl/CMS/Page/Telerik.Web.UI.DialogHandler.aspx","/DesktopModules/News/Telerik.Web.UI.DialogHandler.aspx",
    "/desktopmodules/telerikwebui/radeditorprovider/telerik.web.ui.dialoghandler.aspx","/DesktopModules/dnnWerk.RadEditorProvider/DialogHandler.aspx","/DesktopModules/TNComments/Telerik.Web.UI.DialogHandler.aspx",
    "/DesktopModules/YA.Controls/AngularMain/Telerik.Web.UI.DialogHandler.aspx","/DesktopModules/Base/EditControls/Telerik.Web.UI.DialogHandler.aspx", "/providers/htmleditorproviders/telerik/telerik.web.ui.dialoghandler.aspx",
    "/sitecore/shell/Controls/Rich Text Editor/telerik.web.ui.dialoghandler.aspx", "/sitecore/shell/applications/content manager/telerik.web.ui.dialoghandler.aspx", "/sitecore/shell/Controls/Rich Text Editor/Telerik.Web.UI.DialogHandler.aspx"]

    for TelerikPATH in paths:
        r = requests.get(f'{url}{TelerikPATH}', verify=False, timeout=10, allow_redirects=False, headers=headers)
        if r.status_code == 200:
            if 'Loading the dialog' in r.text:
                print(f'Found - {r.url}')
                with open('telerik_pathfound.txt', 'a+') as output:
                    output.write(f'{r.url}\n')

def main(url):
    r = requests.get(f'http://{url}/', verify=False, timeout=10, allow_redirects=False, headers=headers)
    if r.status_code == 200:
        scan(r.url.strip('/'))
    if r.status_code == 301:
        r = requests.get(f'{r.headers["Location"]}', verify=False, timeout=10, allow_redirects=False, headers=headers)
        if r.status_code == 200:
            scan(r.url.strip('/'))
        else:
            r = requests.get(f'http://www.{url}/', verify=False, timeout=10, allow_redirects=False, headers=headers)
            if r.status_code == 200:
                scan(r.url.strip('/'))
            else:
                r = requests.get(f'https://www.{url}/', verify=False, timeout=10, allow_redirects=False, headers=headers)
                if r.status_code == 200:
                    scan(r.url.strip('/'))
        


if __name__ == "__main__":
    inpFile = input("Enter your List : ")
    threads = []
    with open(inpFile) as urlList_:
        urlList = urlList_.read().splitlines()
    with ThreadPoolExecutor(max_workers=25) as executor:
        for data in urlList:
            threads.append(executor.submit(main, data))
