# PassBrew

PassBrew is a customizable password generation module written in Python. It allows users to create secure, random passwords and passphrases based on specified criteria such as length, character types, and complexity requirements.

## Features

- Generate computer-friendly passwords using secure random methods.
- Generate user-friendly passwords that include customizable parameters like special characters, numbers, and uppercase letters.
- Create memorable passphrases using a selection of random words.
- Flexible settings for minimum and maximum password length, special character counts, and more.

## Installation

To use PassBrew, simply clone the repository and install the required dependencies:

```bash
git clone https://github.com/slavishchenko/passbrew.git
cd passbrew
pip install -r requirements.txt
```

## Usage

To use PassBrew, you can create an instance of `ComputerFriendlyPasswordGenerator`, `UserFriendlyPasswordGenerator`, or `PassphraseGenerator` classes. Below are some examples:

### Basic Computer-Friendly Password Generation

```python
from passbrew.generators.computer_friendly import ComputerFriendlyPasswordGenerator

# Create an instance of ComputerFriendlyPasswordGenerator
computer_friendly_gen = ComputerFriendlyPasswordGenerator()

# Generate a computer-friendly password of desired length
password = computer_friendly_gen.get(16)
print(f'Generated Computer-Friendly Password: {password}')
```

### User-Friendly Password Generation

```python
from passbrew.generators.user_friendly import UserFriendlyPasswordGenerator

# Create an instance of UserFriendlyPasswordGenerator
user_friendly_gen = UserFriendlyPasswordGenerator()

# Set desired amounts for special characters and numbers
UserFriendlyPasswordGenerator.set_char_amount(2)
UserFriendlyPasswordGenerator.set_num_amount(3)

# Generate a user-friendly password
user_password = user_friendly_gen.generate(20)
print(f'Generated User-Friendly Password: {user_password}')
```

### Generate a Passphrase

```python
from passbrew.generators.passphrase import PassphraseGenerator

# Create an instance of PassphraseGenerator
passphrase_gen = PassphraseGenerator()

# Set min and max word count
PassphraseGenerator.set_min_word_count(4)
PassphraseGenerator.set_max_word_count(8)

# Generate a passphrase based on word count
passphrase = passphrase_gen.generate(5, use_word_count=True)
print(f'Generated Passphrase: {passphrase}')
```

## API Reference

For a detailed description of methods and parameters:

- **BasePasswordGenerator**
  - `set_min_length(value: int)`
  - `set_max_length(value: int)`
  - `validate_input(value: int) -> bool`
  - `_get() -> str`

- **ComputerFriendlyPassword**
  - `get(length: int) -> str`
  
- **UserFriendlyPasswordGenerator**
  - `set_char_amount(value: int)`
  - `set_num_amount(value: int)`
  - `generate(length: int) -> str`

- **PassphraseGenerator**
  - `set_min_word_count(value: int)`
  - `set_max_word_count(value: int)`
  - `generate(password_length: int, use_word_count: bool = True) -> str`


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Python's `secrets` module](https://docs.python.org/3/library/secrets.html) for secure random number generation.
```