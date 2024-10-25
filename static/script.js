let userScore = 0;
let computerScore = 0;

async function Mann(choice) {
    document.querySelectorAll('.game-buttons button').forEach(button => {
        button.classList.remove('highlight-red', 'highlight-green');
    });

    let response = await fetch('/play', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `choice=${choice}` // Fixed syntax
    });

    let data = await response.json();

    // Highlight the user's choice
    document.querySelector(`button[onclick="Mann('${choice}')"]`).classList.add('highlight-red');

    // Highlight the computer's choice
    if (data.computer_choice) {
        document.querySelector(`button[onclick="Mann('${data.computer_choice}')"]`).classList.add('highlight-green');
    }

    const resultText = `You chose ${data.user_choice}, computer chose ${data.computer_choice}. You ${data.result}!`; // Fixed syntax
    document.getElementById('result').innerText = resultText;

    if (data.result === 'win') {
        userScore++;
    } else if (data.result === 'lose') {
        computerScore++;
    }

    document.getElementById('userScore').innerText = userScore;
    document.getElementById('computerScore').innerText = computerScore;
}
