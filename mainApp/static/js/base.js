// for copying exact same input from search bar to advanced search bar
function mirrorText() {
    const search1 = document.getElementById('search1');
    const search2 = document.getElementById('search2');
    search2.value = search1.value;
}



// For the dynamic selection and calculation of rent days/price
document.addEventListener('DOMContentLoaded', function() {
    const rentDaysSelect = document.getElementById('rent_days');
    const amountInput = document.getElementById('rent_price');
    const rentPricePerDay = parseFloat(amountInput.placeholder.split(' ')[1]); // Parse the rent price from the placeholder

    function updateAmount() {
        const rentDays = parseInt(rentDaysSelect.value, 10);
        if (!isNaN(rentDays) && rentDays > 0) {
            const totalAmount = rentDays * rentPricePerDay;
            amountInput.placeholder = `RS ${totalAmount}`;
        } else {
            amountInput.placeholder = `RS ${rentPricePerDay}`;
        }
    }

    // Initialize the amount based on the default selected value
    updateAmount();

    // Update the amount when the dropdown value changes
    rentDaysSelect.addEventListener('change', updateAmount);
});
