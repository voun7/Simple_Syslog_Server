document.addEventListener("DOMContentLoaded", function () {
    const socket = io();
    const deviceInput = document.querySelector('input[name="device"]');

    socket.on('new_log', function (data) {
        const filter = deviceInput.value.trim();
        if (filter && !data.log.startsWith(filter + " ")) {
            return;  // Skip log if it doesn't match the filter
        }

        const logList = document.getElementById('log-list');
        const newLogItem = document.createElement('li');
        newLogItem.className = 'log-item';
        newLogItem.textContent = data.log;
        logList.appendChild(newLogItem);
        logList.scrollTop = logList.scrollHeight;
    });
});
