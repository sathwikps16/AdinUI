async function searchFiles() {
    const query = document.getElementById('search-query').value;
    if (!query) {
        alert("Please enter a search term.");
        return;
    }

    const response = await fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
    });

    const files = await response.json();
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (files.error) {
        resultsDiv.innerHTML = `<p>Error: ${files.error}</p>`;
        return;
    }

    if (files.length === 0) {
        resultsDiv.innerHTML = '<p>No files found.</p>';
        return;
    }

    files.forEach(file => {
        const fileElement = document.createElement('div');
        fileElement.className = 'file';

        fileElement.innerHTML = `
            <p>${file.name} (${file.mimeType})</p>
            <button onclick="downloadFile('${file.id}', '${file.name}')">Download</button>
        `;

        resultsDiv.appendChild(fileElement);
    });
}

async function downloadFile(fileId, fileName) {
    const response = await fetch(`/download/${fileId}`);
    if (response.status === 200) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        alert('File downloaded successfully!');
    } else {
        alert('Failed to download file.');
    }
}
