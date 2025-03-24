document.getElementById('languageSwitcher').addEventListener('change', function() {
    var selectedLang = this.value;
    var elements = document.querySelectorAll('.lang');
    elements.forEach(function(element) {
        if (element.classList.contains(selectedLang)) {
            element.style.display = 'block';
        } else {
            element.style.display = 'none';
        }
    });
});
