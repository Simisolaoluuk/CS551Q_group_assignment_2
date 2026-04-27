document.addEventListener('DOMContentLoaded', function() {
    // 1. Enforce max 3 selections for comparison checkboxes
    const compareCheckboxes = document.querySelectorAll('input[name="institution_ids"]');
    const compareForm = document.querySelector('form[action*="compare"]');
    const maxSelections = 3;

    if (compareCheckboxes.length > 0) {
        compareCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const checkedCount = document.querySelectorAll('input[name="institution_ids"]:checked').length;
                
                // Disable unchecked boxes if max is reached
                if (checkedCount >= maxSelections) {
                    compareCheckboxes.forEach(box => {
                        if (!box.checked) box.disabled = true;
                    });
                } else {
                    compareCheckboxes.forEach(box => {
                        box.disabled = false;
                    });
                }
            });
        });
    }

    // 2. Validate form submission (must select at least 2)
    if (compareForm) {
        compareForm.addEventListener('submit', function(event) {
            const checkedCount = document.querySelectorAll('input[name="institution_ids"]:checked').length;
            if (checkedCount < 2) {
                event.preventDefault();
                alert('Please select at least 2 institutions to compare.');
            }
        });
    }
});