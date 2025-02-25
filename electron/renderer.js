const info = document.getElementById('info')
info.innerText = `Versions: chrome=${window.versions.chrome()}, node=${window.versions.node()}, electron=${window.versions.electron()}`
console.log(`outer: ping=${ping}`)

// Note: can't call this 'ping' because window.ping is also exposed as a global 'ping' var
const pingEl = document.getElementById('ping')
async function populatePingElement() {
    console.log('enter f')
    pingEl.innerText = `loading`
    try {
        const resp = await window.ping.response()
        pingEl.innerText = `Main process replied to ping request with: ${resp}`
    } catch (err) {
        pingEl.innerText = `Error getting ping: ${err.message}`
    }
}
populatePingElement()