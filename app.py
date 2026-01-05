from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import random
import os
from typing import Dict, Any, List

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session

# Game constants
MAX_ATTEMPTS = 6
WORDS = [
    'giraffe', 'elephant', 'dolphin', 'kangaroo', 'octopus',
    'algorithm', 'database', 'firewall', 'keyboard', 'monitor',
    'waterfall', 'mountain', 'volcano', 'blizzard', 'rainbow',
    'spaghetti', 'avocado', 'chocolate', 'pineapple', 'sandwich',
    'microscope', 'telescope', 'laboratory', 'molecule', 'velocity',
    'badminton', 'baseball', 'cricket', 'football', 'hockey',
    'guitar', 'trumpet', 'violin', 'melody', 'harmony',
    'galaxy', 'nebula', 'planet', 'rocket', 'universe',
    'airplane', 'bicycle', 'scooter', 'tractor', 'zeppelin'
]


def get_hangman_stage(tries: int) -> str:
    """Return the appropriate hangman stage based on number of incorrect tries."""
    stages = [
        # Initial empty state (0 incorrect guesses)
        """
           --------
           |      |
           |      
           |    
           |      
           |     
           -
        """,
        # Head (1 incorrect guess)
        """
           --------
           |      |
           |      O
           |    
           |      
           |     
           -
        """,
        # Head, torso (2 incorrect guesses)
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |     
           -
        """,
        # Head, torso, one arm (3 incorrect guesses)
        """
           --------
           |      |
           |      O
           |     \|
           |      |
           |     
           -
        """,
        # Head, torso, both arms (4 incorrect guesses)
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |      
           -
        """,
        # Head, torso, both arms, one leg (5 incorrect guesses)
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / 
           -
        """,
        # Final state: complete hangman (6 incorrect guesses)
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / \
           -
        """
    ]
    return stages[min(tries, len(stages) - 1)]


def init_game() -> Dict[str, Any]:
    """Initialize a new game state."""
    word = random.choice(WORDS)
    return {
        'word': word,
        'word_display': ['_'] * len(word),
        'guessed_letters': [],  # Using list instead of set
        'attempts_left': MAX_ATTEMPTS,
        'game_over': False,
        'won': False
    }


def update_game_state(game_state: Dict[str, Any], guess: str) -> None:
    """Update the game state based on the player's guess."""
    if game_state['game_over'] or guess in game_state['guessed_letters']:
        return

    game_state['guessed_letters'].append(guess)

    if guess in game_state['word']:
        # Update word display with correctly guessed letters
        for i, letter in enumerate(game_state['word']):
            if letter == guess:
                game_state['word_display'][i] = letter

        # Check if player has won
        if '_' not in game_state['word_display']:
            game_state['won'] = True
            game_state['game_over'] = True
    else:
        # Incorrect guess
        game_state['attempts_left'] -= 1
        if game_state['attempts_left'] == 0:
            game_state['game_over'] = True


@app.route('/')
def index():
    """Render the main game page."""
    if 'game_state' not in session:
        session['game_state'] = init_game()

    game_state = session['game_state']

    return render_template(
        'index.html',
        hangman_display=get_hangman_stage(MAX_ATTEMPTS - game_state['attempts_left']),
        word_display=' '.join(game_state['word_display']),
        guessed_letters=', '.join(sorted(game_state['guessed_letters'])),
        message='' if not game_state['game_over'] else
        'You won!' if game_state['won'] else
        f'Game Over! The word was: {game_state["word"]}'
    )


@app.route('/guess', methods=['POST'])
def guess():
    """Handle a letter guess from the player."""
    if 'game_state' not in session:
        return jsonify({'redirect': url_for('index')})

    data = request.get_json()
    guess_letter = data.get('letter', '').lower()

    if len(guess_letter) == 1 and guess_letter.isalpha():
        update_game_state(session['game_state'], guess_letter)
        session.modified = True  # Mark session as modified to save changes

    return jsonify({})


@app.route('/new_game', methods=['POST'])
def new_game():
    """Start a new game."""
    session['game_state'] = init_game()
    session.modified = True  # Mark session as modified to save changes
    return jsonify({'redirect': url_for('index')})


if __name__ == '__main__':
    app.run(debug=True)
