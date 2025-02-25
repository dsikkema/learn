/**
 * Loads before other js, has access to DOM but also a subset of node and electron APIs
 */
const { contextBridge, ipcRenderer } = require('electron')

/**
 * contextBridge.exposeInMainWorld('apiKey', 'api') exposes functions to be able to be
 * called in renderer js processes. The 'apiKey' it exposes is made available as both
 * a global apiKey and a window.apiKey variable.
 */
contextBridge.exposeInMainWorld('versions', 
    {
        node: () => process.versions.node,
        chrome: () => process.versions.chrome,
        electron: () => process.versions.electron
    }
);

contextBridge.exposeInMainWorld('ping',
    {
        response: () => ipcRenderer.invoke('ping')
    }
)