class Calculator{

    constructor(previousOperandTextElement, currentOperandTextElement){
        this.previousOperandTextElement = previousOperandTextElement;
        this.currentOperandTextElement = currentOperandTextElement;
        this.clear();
        this.justReturned = false;
    }

    clear(){
        this.currentOperand = '';
        this.previousOperand= '';
        this.operation = undefined;
    }

    delete(){
        this.currentOperand = this.currentOperand.toString().slice(0,-1);
    }

    appendNumber(number){
        if(number.toString() === '.' && this.currentOperand.toString().includes('.'))
            return;
        if(this.justReturned){
            this.currentOperand = '';
            this.justReturned =false;
        }
        this.currentOperand = this.currentOperand.toString() + number.toString();
    }

    chooseOperation(operation){
        if(this.currentOperand === '') return
        if(this.previousOperand !== ''){
            this.compute();
        }
        this.operation = operation;
        this.previousOperand = this.currentOperand;
        this.currentOperand = '';
    }

    compute(){
        let computation
        const prev = parseFloat(this.previousOperand);
        const curr = parseFloat(this.currentOperand);
        if(isNaN(prev) || isNaN(curr)) return;
        switch(this.operation){
            case '+' :
                computation = curr + prev;
                break;
            case '×' :
                computation = curr * prev;
                break;
            case '-' :
                computation = prev - curr;
                break;
            case '÷' :
                computation = prev / curr;
                break;
            default: return;
        }
        this.currentOperand = computation;
        this.operation = undefined;
        this.previousOperand = '';
        this.justReturned = true;
    }
    
    getDisplayNumber(number){
        const stringNumber = number.toString();
        const integerDigits = parseFloat(stringNumber.split('.')[0]);
        const decimalDigits = stringNumber.split('.')[1];
        let integerDisplay;
        if(isNaN(integerDigits)){
            integerDisplay = '';
        }else{
            integerDisplay = integerDigits.toLocaleString('en', {maximumFractionDigits: 0})
        }

        if(decimalDigits != null){
            return `${integerDisplay}.${decimalDigits}`
        }else{
            return integerDisplay;
        }
    }

    updateDisplay(){
        this.currentOperandTextElement.innerText = this.getDisplayNumber(this.currentOperand);
        this.previousOperandTextElement.innerText = this.previousOperand;
        if(this.operation != null){
            this.previousOperandTextElement.innerText = 
                                `${this.getDisplayNumber(this.previousOperand)} ${this.operation}`
        }
    }

}

const numberButtons = document.querySelectorAll('[data-number]')
const operationButtons = document.querySelectorAll('[data-operation')
const equalsButton = document.querySelector('[data-equals]')
const deleteButton = document.querySelector('[data-delete]')
const clearButton = document.querySelector('[data-clear]')
const previousOperandTextElement = document.querySelector('[data-previous-operand]')
const currentOperandTextElement = document.querySelector('[data-current-operand]')

const calculator = new Calculator(previousOperandTextElement, currentOperandTextElement);


document.addEventListener('keyup', (event) => {
    const keyName = event.key;
    const numKey = parseInt(keyName);
    if(!isNaN(numKey) || keyName === '.'){
        calculator.appendNumber(keyName);
    }else if(keyName === 'Backspace')
    {
        if(event.ctrlKey){
            calculator.clear()
        }else{
        calculator.delete();
        }
    }else if(keyName === 'Enter'){
        calculator.compute();
    }else {
        switch(keyName){
            case '+':
                calculator.chooseOperation('+')
                break;
            case '-':
                calculator.chooseOperation('-')
                break;
            case '*':
                calculator.chooseOperation('×')
                break;
            case '/':
                calculator.chooseOperation('÷')
                break;
            default: break;
        }
    }
    calculator.updateDisplay();
})

numberButtons.forEach(button => {
    button.addEventListener('click', () => {
        calculator.appendNumber(button.innerText);
        calculator.updateDisplay();
    })
})

clearButton.addEventListener('click', button => {
    calculator.clear();
    calculator.updateDisplay();
})

deleteButton.addEventListener('click', button => {
    calculator.delete();
    calculator.updateDisplay();
})

operationButtons.forEach(button => {
    button.addEventListener('click', () => {
        calculator.chooseOperation(button.innerText);
        calculator.updateDisplay();
    })
})

equalsButton.addEventListener('click', button => {
    calculator.compute();
    calculator.updateDisplay();
})