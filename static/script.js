let userScore = 0;
let computerScore = 0;

async function Mann(choice) {
    document.querySelectorAll('.game-buttons button').forEach(button => {
        button.classList.remove('highlight-red', 'highlight-green');
    });

    let Aman = await fetch('/play', {
        method: 'post',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `choice=${choice}`
    });

    let Mann2 = await Aman.json();

    // Highlight the user's choice
    document.querySelector(`button[onclick="Mann('${choice}')"]`).classList.add('highlight-red');

    // Highlight the computer's choice
    if (Mann2.computer_choice) {
        document.querySelector(`button[onclick="Mann('${Mann2.computer_choice}')"]`).classList.add('highlight-green');
    }

    const resultText = `You chose ${Mann2.user_choice}, computer chose ${Mann2.computer_choice}. You ${Mann2.result}!`;
    document.getElementById('result').innerText = resultText;

    if (Mann2.result === 'win') {
        userScore++;
    } else if (Mann2.result === 'lose') {
        computerScore++;
    }

    document.getElementById('userScore').innerText = userScore;
    document.getElementById('computerScore').innerText = computerScore;
}
