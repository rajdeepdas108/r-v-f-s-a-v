// Handle biometric capture and voting
async function captureAndVote(candidate) {
    const video = document.getElementById('videoFeed');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    const imageData = canvas.toDataURL('image/jpeg');
    const voterId = document.getElementById('voterId').value;

    const formData = new FormData();
    formData.append('image', dataURLtoBlob(imageData), 'biometric.jpg');
    formData.append('voter_id', voterId);
    formData.append('candidate', candidate);

    try {
        const response = await fetch('/api/vote', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        if(result.error) throw new Error(result.error);
        
        updateResults();
        showVoteReceipt(result.tx_hash, result.merkle_proof);
    } catch(error) {
        showError(error.message);
    }
}

// Update results display
async function updateResults() {
    try {
        const response = await fetch('/api/results');
        const data = await response.json();
        
        document.getElementById('merkleRoot').textContent = data.merkle_root;
        document.getElementById('totalVotes').textContent = data.total_votes;
        
        // Update chart
        updateChart(data.results);
    } catch(error) {
        showError('Failed to fetch results');
    }
}