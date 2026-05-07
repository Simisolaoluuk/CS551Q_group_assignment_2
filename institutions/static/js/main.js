document.addEventListener('DOMContentLoaded', function() {
    const compareForms = document.querySelectorAll('form[action*="compare"]');
    const maxSelections = 3;

    compareForms.forEach(function(compareForm) {
        const compareCheckboxes = compareForm.querySelectorAll('input[name="institution_ids"]');

        if (compareCheckboxes.length > 0) {
            compareCheckboxes.forEach(function(checkbox) {
                checkbox.addEventListener('change', function() {
                    const checkedCount = compareForm.querySelectorAll('input[name="institution_ids"]:checked').length;

                    compareCheckboxes.forEach(function(box) {
                        box.disabled = checkedCount >= maxSelections && !box.checked;
                    });
                });
            });
        }

        compareForm.addEventListener('submit', function(event) {
            const checkedCount = compareForm.querySelectorAll('input[name="institution_ids"]:checked').length;

            if (checkedCount < 2) {
                event.preventDefault();
                alert('Please select at least 2 institutions to compare.');
                return;
            }

            if (checkedCount > maxSelections) {
                event.preventDefault();
                alert('You can compare a maximum of 3 institutions.');
            }
        });
    });
});