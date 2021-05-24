/**
 * @param  {HTMLFormElement} formElement
 * Observes changes of values of a html form. If values of user-entry
 * widget in the form changing, enables form submit button, otherwise
 * keeps it disabled (to prevent sending the same data that was
 * provident for the form by default).
 */
class FormChangesDetector {
    constructor(formElement) {
        this.formElement = formElement
        this.submitButton = this.getSubmitButton()

        this.checkForChanges()
        
        this.formElement.addEventListener('input', event => {
            this.checkForChanges()
        })
    }

    getSubmitButton() {
        for (let el of this.formElement) {
            if (el.type === 'submit') {
                return el
            } 
        }
        throw 'cannot find a submit button on the form'
    }

    inputChanged(input) {
        return input.value != input.defaultValue
    }

    checkForChanges() {
        for (let el of this.formElement.elements) {
            if (this.inputChanged(el)) {
                this.submitButton.disabled = false
                break
            } else {
                this.submitButton.disabled = true
            }
        }
    }
}
