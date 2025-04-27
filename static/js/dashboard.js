document.addEventListener('DOMContentLoaded', function() {
    const redeemForm = document.getElementById('redeem-form');
    const redeemResult = document.getElementById('redeem-result');
    
    if (redeemForm) {
        redeemForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const keyInput = document.getElementById('key-input');
            const key = keyInput.value.trim();
            
            if (!key) {
                showResult('Please enter a key', 'error');
                return;
            }
            
            fetch('/redeem_key', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `key=${encodeURIComponent(key)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showResult(data.message, 'success');
                    // Refresh the page to update user info
                    setTimeout(() => location.reload(), 1500);
                } else {
                    showResult(data.message, 'error');
                }
            })
            .catch(error => {
                showResult('An error occurred. Please try again.', 'error');
                console.error('Error:', error);
            });
        });
    }
    
    function showResult(message, type) {
        redeemResult.textContent = message;
        redeemResult.className = type;
    }
});