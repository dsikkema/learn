const { app, BrowserWindow, ipcMain } = require('electron/main')
const path = require('node:path')
/**
 * app: controls app event lifecycle
 * BrowserWindow: manages app windows
 * 
 * While window is running, it's in a separate 'renderer' process, but this file controls
 * the 'main' process
 */
const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    })

    win.loadFile('index.html')
}

/**
 * app is a node "event emitter". whenReady() is a wrapper provided by electron to
 * address particular concerns with the 'ready' event, but it wraps the typical
 * node.js event listener format which is:
ee1.on('foo', () => {
    doStuff();
});
 */

app.whenReady().then(() => {
    ipcMain.handle('ping', () => 'pong')
    createWindow()
})
