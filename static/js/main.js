// Initialize all tooltips
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Initialize all popovers
const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl, {
        html: true,
        trigger: 'hover'
    });
});

// Add fade-in animation to cards
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.classList.add('fade-in');
    });
});

// Dynamic search functionality for tables
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('tableSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchText = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchText) ? '' : 'none';
            });
        });
    }
});

// Employment details toggle in graduate form
document.addEventListener('DOMContentLoaded', function() {
    const isEmployedCheckbox = document.getElementById('id_is_employed');
    if (isEmployedCheckbox) {
        function toggleEmploymentDetails() {
            const employmentDetails = document.getElementById('employment-details');
            if (employmentDetails) {
                employmentDetails.style.display = isEmployedCheckbox.checked ? 'block' : 'none';
            }
        }
        
        isEmployedCheckbox.addEventListener('change', toggleEmploymentDetails);
        toggleEmploymentDetails();
    }
});

// File upload preview
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileName = this.files[0]?.name;
            const fileLabel = document.querySelector('.custom-file-label');
            if (fileLabel) {
                fileLabel.textContent = fileName || 'Choose file';
            }
        });
    }
});

// Chart color scheme
const chartColors = {
    primary: '#2c3e50',
    secondary: '#3498db',
    success: '#27ae60',
    warning: '#f1c40f',
    danger: '#e74c3c',
    light: '#f8f9fa'
};

// Function to format numbers with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Update stats cards with animation
function updateStatsCard(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        const duration = 1000;
        const steps = 50;
        const increment = value / steps;
        let current = 0;
        let step = 0;
        
        const timer = setInterval(() => {
            current += increment;
            element.textContent = formatNumber(Math.round(current));
            step++;
            
            if (step >= steps) {
                element.textContent = formatNumber(value);
                clearInterval(timer);
            }
        }, duration / steps);
    }
}
