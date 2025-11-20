const params = new URLSearchParams(location.search)
const name = params.get('name')

document.getElementById('title').textContent = name

const responseBox = document.getElementById('response')

function setResponse(text) {
    responseBox.textContent = text
}

function loadLogs() {
    fetch('/api/service_logs/' + encodeURIComponent(name))
        .then(r => r.json())
        .then(data => {
            const box = document.getElementById('logs')
            if (data.error) {
                box.textContent = ''
                return
            }
            box.textContent = data.lines.join('\n')
        })
}

document.getElementById('start').onclick = function() {
    fetch('/api/start/' + encodeURIComponent(name), { method: 'POST' })
        .then(r => r.json())
        .then(j => {
            setResponse(JSON.stringify(j))
            loadLogs()
        })
}

document.getElementById('stop').onclick = function() {
    fetch('/api/stop/' + encodeURIComponent(name), { method: 'POST' })
        .then(r => r.json())
        .then(j => {
            setResponse(JSON.stringify(j))
            loadLogs()
        })
}

document.getElementById('refresh').onclick = loadLogs

loadLogs()
