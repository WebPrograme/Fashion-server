// Description: This file contains the javascript code for the multi-step form and to show the Ready2Go modal when reloaded.

// This function is used to navigate to the next form step
const navigateToFormStep = (stepNumber) => {
    document.querySelectorAll(".form-step").forEach((formStepElement) => {
        formStepElement.classList.add("d-none");
    });

    document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
        formStepHeader.classList.add("form-stepper-unfinished");
        formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
    });

    document.querySelector("#step-" + stepNumber).classList.remove("d-none");

    if (parseInt(stepNumber) >= 3) {
        stepNumber = 3;
    }
    
    const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
    formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
    formStepCircle.classList.add("form-stepper-active");

    document.querySelector('li[step="1"] a').removeAttribute("onclick");
    document.querySelector('li[step="2"] a').removeAttribute("onclick");
    document.querySelector('li[step="3"] a').removeAttribute("onclick");

    for (let index = 0; index < stepNumber; index++) {
        const formStepCircle = document.querySelector('li[step="' + index + '"]');
        const formStepLink = document.querySelector('li[step="' + index + '"] a');
        
        if (formStepCircle) {
            formStepLink.setAttribute("onclick", "navigateBackFormStep(" + index + ");");

            formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
            formStepCircle.classList.add("form-stepper-completed");
        }
    }
};

// This function is used to navigate to the previous form step
const navigateBackFormStep = (stepNumber) => {
    const stepList = ['Gender', 'Type', 'Input']
    document.querySelectorAll(".form-step").forEach((formStepElement) => {
        formStepElement.classList.add("d-none");
    });
    
    document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
        formStepHeader.classList.add("form-stepper-unfinished");
        formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
    });
    
    document.querySelector("#step-" + stepNumber).classList.remove("d-none");

    if (parseInt(stepNumber) >= 3) {
        stepNumber = 3;
    }
    const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
    formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
    formStepCircle.classList.add("form-stepper-active");

    for (let index = stepNumber; index < 4; index++) {
        const stepHeader = document.querySelector('.step-' + index + '-header');
        stepHeader.innerHTML = stepList[index - 1];
    }

    document.querySelector('li[step="1"] a').removeAttribute("onclick");
    document.querySelector('li[step="2"] a').removeAttribute("onclick");
    document.querySelector('li[step="3"] a').removeAttribute("onclick");

    for (let index = 0; index < stepNumber; index++) {
        const formStepCircle = document.querySelector('li[step="' + index + '"]');
        const formStepLink = document.querySelector('li[step="' + index + '"] a');
        
        if (formStepCircle) {
            formStepLink.setAttribute("onclick", "navigateBackFormStep(" + index + ");");
            
            formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
            formStepCircle.classList.add("form-stepper-completed");
        }
    }
};

// This function is used to submit the gender and navigate to the next form step
document.querySelectorAll('.form-btn-gender').forEach((formBtnGender) => {
    formBtnGender.addEventListener('click', () => {
        const gender = formBtnGender.innerHTML;

        document.querySelector('.step-1-header').innerHTML = gender;

        localStorage.setItem('gender', gender)

        navigateToFormStep(2);
    });
});

// This function is used to submit the type and navigate to the next form step
document.querySelectorAll('.form-btn-type').forEach((formBtnType) => {
    formBtnType.addEventListener('click', (e) => {
        if (e.target.nodeName === 'DIV') {
            const type = formBtnType.innerHTML;
    
            if (type.includes('Link')) {
                navigateToFormStep(3);
                document.querySelector('.step-2-header').innerHTML = 'Link';
            } else if (type.includes('Number')) {
                navigateToFormStep(4);
                document.querySelector('.step-2-header').innerHTML = 'Number';
            } else if (type.includes('Image')) {
                navigateToFormStep(5);
                document.querySelector('.step-2-header').innerHTML = 'Image';
            }
        }
    });
});

// This function is used to reload the ready2go items
document.getElementById('ready2go-btn-reload').addEventListener('click', () => {
    window.location.reload();
    localStorage.setItem('ReloadReady2Go', 'true');
});

// This function is used to navigate to the ready2go items if the page is reloaded
window.onload = function() {
    if (localStorage.getItem('ReloadReady2Go') === 'true') {
        navigateToFormStep(5);
        document.querySelector('.step-2-header').innerHTML = 'Image';
        $("#ready2goBackdrop").modal('show')
        localStorage.removeItem('ReloadReady2Go');
    }
}

// This is used to automatically navigate to the next form step if the user has already selected a gender before
const localStorageGender = localStorage.getItem('gender');

if (localStorageGender !== null) {
    document.querySelector('.step-1-header').innerHTML = localStorageGender;

    localStorage.setItem('gender', localStorageGender)

    navigateToFormStep(2);
}