function loadServices() {
    fetch('/api/status')
        .then(r => r.json())
        .then(data => {
            const div = document.getElementById('list')
            div.innerHTML = ''

            for (const name in data) {
                const row = document.createElement('div')

                const link = document.createElement('a')
                link.href = 'service/?name=' + encodeURIComponent(name)
                link.textContent = name

                const state = document.createElement('span')
                state.textContent = data[name] ? ' (running)' : ' (stopped)'

                row.appendChild(link)
                row.appendChild(state)
                div.appendChild(row)
            }
        })
}

function loadGlobalLogs() {
    fetch('/api/logs')
        .then(r => r.json())
        .then(data => {
            const box = document.getElementById('globallogs')
            if (!data.lines) {
                box.textContent = ''
                return
            }
            box.textContent = data.lines.join('\n')
        })
}

document.getElementById('shutdown').onclick = function() {
    fetch('/api/shutdown', { method: 'POST' })
        .then(r => r.json())
        .then(j => {
            document.getElementById('shutdown_response').textContent =
                JSON.stringify(j)
        })
}

loadServices()
loadGlobalLogs()
