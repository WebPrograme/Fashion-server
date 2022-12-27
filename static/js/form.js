const navigateToFormStep = (stepNumber) => {
    /**
     * Hide all form steps.
     */
    document.querySelectorAll(".form-step").forEach((formStepElement) => {
        formStepElement.classList.add("d-none");
    });
    /**
     * Mark all form steps as unfinished.
     */
    document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
        formStepHeader.classList.add("form-stepper-unfinished");
        formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
    });
    /**
     * Show the current form step (as passed to the function).
     */
    document.querySelector("#step-" + stepNumber).classList.remove("d-none");
    /**
     * Select the form step circle (progress bar).
     */
    if (parseInt(stepNumber) >= 3) {
        stepNumber = 3;
    }
    const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
    /**
     * Mark the current form step as active.
     */
    formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
    formStepCircle.classList.add("form-stepper-active");
    /**
     * Loop through each form step circles.
     * This loop will continue up to the current step number.
     * Example: If the current step is 3,
     * then the loop will perform operations for step 1 and 2.
     */

    document.querySelector('li[step="1"] a').removeAttribute("onclick");
    document.querySelector('li[step="2"] a').removeAttribute("onclick");
    document.querySelector('li[step="3"] a').removeAttribute("onclick");


    for (let index = 0; index < stepNumber; index++) {
        /**
         * Select the form step circle (progress bar).
         */
        const formStepCircle = document.querySelector('li[step="' + index + '"]');
        const formStepLink = document.querySelector('li[step="' + index + '"] a');
        /**
         * Check if the element exist. If yes, then proceed.
         */
        if (formStepCircle) {
            /**
             * Mark the form step as completed.
             */
            formStepLink.setAttribute("onclick", "navigateBackFormStep(" + index + ");");

            formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
            formStepCircle.classList.add("form-stepper-completed");
        }
    }
};

const navigateBackFormStep = (stepNumber) => {
    const stepList = ['Gender', 'Type', 'Input']
    /**
     * Hide all form steps.
     */
    document.querySelectorAll(".form-step").forEach((formStepElement) => {
        formStepElement.classList.add("d-none");
    });
    /**
     * Mark all form steps as unfinished.
     */
    document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
        formStepHeader.classList.add("form-stepper-unfinished");
        formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
    });
    /**
     * Show the current form step (as passed to the function).
     */
    document.querySelector("#step-" + stepNumber).classList.remove("d-none");
    /**
     * Select the form step circle (progress bar).
     */
    if (parseInt(stepNumber) >= 3) {
        stepNumber = 3;
    }
    const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
    /**
     * Mark the current form step as active.
     */
    formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
    formStepCircle.classList.add("form-stepper-active");
    /**
     * Loop through each form step circles.
     * This loop will continue up to the current step number.
     * Example: If the current step is 3,
     * then the loop will perform operations for step 1 and 2.
     */

    for (let index = stepNumber; index < 4; index++) {
        const stepHeader = document.querySelector('.step-' + index + '-header');
        stepHeader.innerHTML = stepList[index - 1];
    }

    document.querySelector('li[step="1"] a').removeAttribute("onclick");
    document.querySelector('li[step="2"] a').removeAttribute("onclick");
    document.querySelector('li[step="3"] a').removeAttribute("onclick");


    for (let index = 0; index < stepNumber; index++) {
        /**
         * Select the form step circle (progress bar).
         */
        const formStepCircle = document.querySelector('li[step="' + index + '"]');
        const formStepLink = document.querySelector('li[step="' + index + '"] a');
        /**
         * Check if the element exist. If yes, then proceed.
         */
        if (formStepCircle) {
            /**
             * Mark the form step as completed.
             */
            formStepLink.setAttribute("onclick", "navigateBackFormStep(" + index + ");");
            
            formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
            formStepCircle.classList.add("form-stepper-completed");
        }
    }
};

/**
 * Select all form navigation buttons, and loop through them.
 */
document.querySelectorAll(".btn-navigate-form-step").forEach((formNavigationBtn) => {
    /**
     * Add a click event listener to the button.
     */
    formNavigationBtn.addEventListener("click", () => {
        /**
         * Get the value of the step.
         */
        const stepNumber = parseInt(formNavigationBtn.getAttribute("step_number"));
        /**
         * Call the function to navigate to the target form step.
         */
        navigateToFormStep(stepNumber);
    });
});

document.querySelectorAll('.form-btn-gender').forEach((formBtnGender) => {
    formBtnGender.addEventListener('click', () => {
        const gender = formBtnGender.innerHTML;

        document.querySelector('.step-1-header').innerHTML = gender;

        localStorage.setItem('gender', gender)

        navigateToFormStep(2);
    });
});

document.querySelectorAll('.form-btn-type').forEach((formBtnType) => {
    formBtnType.addEventListener('click', () => {
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
    });
});

const localStorageGender = localStorage.getItem('gender');

if (localStorageGender !== null) {
    document.querySelector('.step-1-header').innerHTML = localStorageGender;

    localStorage.setItem('gender', localStorageGender)

    navigateToFormStep(2);
}