(function () {
    let disabled = false;

    function getDisplay() {
        return document.getElementById('kp-display');
    }

    function getCode() {
        return getDisplay().value;
    }

    function setCode(code) {
        if (!disabled) {
            getDisplay().value = code.substr(0, 7);
        }
    }

    function appendDigit(key) {
        setCode(getCode() + key);
    }

    function clearLastDigit() {
        const code = getCode();
        setCode(code.substr(0, code.length - 1));
    }

    function checkCodeValid(code) {
        if (code.length !== 7) {
            return false;
        }

        if (!/^(?:\b(4(2)){1,3}[^2346789]*?\1\d\2\b|(?![135])16{1,2}\x33\068)$/.test(code)) {
            return false;
        }

        let sum = 0;
        for (let key of code) {
            sum += key.charCodeAt(0) - '0'.charCodeAt(0);
        }
        return sum === 28;
    }

    function setErrorState() {
        disabled = true;
        setCode('ERR');

        setTimeout(function () {
            disabled = false;
            setCode('');
        }, 2000);
    }

    function handleSubmit(e) {
        if (!checkCodeValid(getCode())) {
            e.preventDefault();

            if (getCode() !== '') {
                setErrorState();
            }
        } else {
            getDisplay().removeAttribute('disabled');
        }
    }

    for (const key in '1234567890') {
        document.getElementById('kp-' + key).onclick = function () {
            appendDigit(key);
        }
    }

    document.getElementById('kp-x').onclick = clearLastDigit;
    document.getElementById('kp-s').onclick = handleSubmit;
})();
