from urllib.parse import urljoin
from requests import post, Response
from shutil import make_archive
from dotenv import load_dotenv
from os import getenv

load_dotenv('secret.env')

USERNAME = getenv('PYTHONANYWHERE_USERNAME')
TOKEN = getenv('PYTHONANYWHERE_TOKEN')
MAIN_URL = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}/"
MAIN_REMOTE_FOLDER = 'mysite'
ZIP_FOLDER = MAIN_REMOTE_FOLDER + '.zip'
LOCAL_MAIN_FOLDER = 'backend'

def zipFolder(source, destination):
    make_archive(destination.replace(".zip", ""), "zip", source)

def createUrl(actualUrl):
    return urljoin(MAIN_URL, actualUrl)

def logResponse(response: Response):
    print(response.url, response.status_code, 'Success' if response.status_code == 200 else "You're probably fucked...")

def getConsoleId():
    url = createUrl("consoles")

    response = post(
        url,
        headers={"Authorization": f"Token {TOKEN}"},
        data={"executable": "/bin/bash"}
    )
    
    logResponse(response)

    console = response.json()[0]
    consoleId = console["id"]

    return consoleId

def executeCommand(command):
    consoleId = getConsoleId()

    response = post(
        createUrl(f'consoles/{consoleId}/send_input/'),
        headers={"Authorization": f"Token {TOKEN}"},
        data={"input": command + "\n"}
    )

    logResponse(response)

def sendFile(source, destination):
    remoteDestination = f"/home/{USERNAME}/{destination}"

    with open(source, "rb") as file:
        response = post(
            f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{remoteDestination}/",
            headers={"Authorization": f"Token {TOKEN}"},
            files={"content": file}
        )

        logResponse(response)

def reload():
    domainName = f"{USERNAME}.pythonanywhere.com"
    url = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}/webapps/{domainName}/reload/"

    response = post(
        url, 
        headers={"Authorization": f"Token {TOKEN}"}
    )

    logResponse(response)

def deleteMainFolder():
    executeCommand(f'rm -r {MAIN_REMOTE_FOLDER}')

def createMainFolder():
    executeCommand(f'mkdir -p {MAIN_REMOTE_FOLDER}')

def unzipMainFolder():
    executeCommand(f'unzip -o {MAIN_REMOTE_FOLDER}.zip -d {MAIN_REMOTE_FOLDER}')


def sendMainFolder():
    sendFile(ZIP_FOLDER, ZIP_FOLDER)

def zipMainFolder():
    return zipFolder(LOCAL_MAIN_FOLDER, MAIN_REMOTE_FOLDER)


if __name__ == '__main__':
    deleteMainFolder()
    createMainFolder()
    zipMainFolder()
    sendMainFolder()
    unzipMainFolder()
    reload()