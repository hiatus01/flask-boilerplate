document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.flash').forEach(flash => {
        flash.addEventListener('click', function() {
            this.remove();
        });
    });
});