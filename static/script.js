document.getElementById('x').addEventListener('input', function (e) {
    this.value = this.value.replace(/[^0-9]/g, '');
});

async function calculateResult(event) {
    event.preventDefault();
    const form = document.getElementById('poisson-form');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const formData = new FormData(form);
    const data = {
        probability_type: formData.get('probability_type'),
        lam: parseFloat(formData.get('lam')),
        x: parseInt(formData.get('x'), 10)
    };

    try {
        const response = await fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();

        document.getElementById('initial-description').style.display = 'none';
        document.getElementById('result-description').style.display = 'block';

        document.getElementById('value-x').innerText = data.x;
        document.getElementById('value-lam').innerText = data.lam;
        document.getElementById('calculation-type').innerHTML = `\\(${result.langkah.rumus}\\)`;

        let calculationTitle = "";
        if (data.probability_type === "exact") {
            calculationTitle = `P(X = ${data.x})`;
        } else if (data.probability_type === "less_than") {
            calculationTitle = `P(X < ${data.x})`;
        } else if (data.probability_type === "at_most") {
            calculationTitle = `P(X \\leq ${data.x})`;
        } else if (data.probability_type === "greater_than") {
            calculationTitle = `P(X > ${data.x})`;
        } else if (data.probability_type === "at_least") {
            calculationTitle = `P(X \\geq ${data.x})`;
        }
        document.getElementById('calculation-title').innerHTML = `\\(\\small ${calculationTitle}\\)`;

        let stepsContent = "";
        if (data.probability_type === "greater_than" && result.langkah) {
            stepsContent += `\\(${result.langkah.summary}\\)`;
        } else if (data.probability_type === "at_least" && result.langkah) {
            stepsContent += `\\(${result.langkah.summary}\\)`;
        } else if ((data.probability_type === "less_than" || data.probability_type === "at_most") && result.langkah.steps) {
            result.langkah.steps.forEach(step => {
                stepsContent += `\\(${step}\\)<br>`;
            });
            stepsContent += `\\(${result.langkah.summary}\\)`;
        } else {
            stepsContent = `\\(${result.langkah.langkah1}\\)\\(${result.langkah.langkah2}\\)\\(${result.langkah.langkah3 || ""}\\)`;
        }
        document.getElementById('calculation-steps').innerHTML = stepsContent;

        document.getElementById('final-result-content').innerHTML = `\\( ${result.hasil} \\)`;
        MathJax.typeset();
    } catch (error) {
        console.error('Error:', error);
    }
}

function resetPage() {
    document.getElementById('initial-description').style.display = 'block';
    document.getElementById('result-description').style.display = 'none';
    document.getElementById('description').style.backgroundColor = '#ffffff';
    document.getElementById('poisson-form').reset();
}

document.getElementById('probability_type').addEventListener('change', function() {
    document.getElementById('initial-description').style.display = 'block';
    document.getElementById('result-description').style.display = 'none';
});