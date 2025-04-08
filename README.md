# Password Generator Module

## Overview

The Password Generator module is a Python-based tool for generating secure passwords and user-friendly passphrases. It allows users to create customizable passwords that meet various security criteria, ensuring both strength and memorability.

## Features

- **Customizable Length**: Set minimum and maximum lengths for generated passwords.
- **User-Friendly Passwords**: Generate passwords that are easy to remember yet secure.
- **Passphrase Generation**: Create passphrases using random words, ensuring they're memorable and secure.
- **Special Characters and Numbers**: Optionally include special characters, numbers, and spaces for added complexity.
- **Validation**: Input lengths are validated against set constraints to prevent incorrect usage.

## Installation

To use this module, ensure you have Python installed on your system. No external dependencies are required beyond the standard library.

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/password-generator.git
    cd password-generator
    ```

2. Ensure that the `words.txt` file is located in the same directory as your script for word selection.

## Usage

Here’s an example of how to use the Password Generator module to create passwords and passphrases:

```python
from password import UserFriendlyPassword, Passphrase

# Create an instance of UserFriendlyPassword
friendly_password_generator = UserFriendlyPassword()

# Generate a user-friendly password of length 16
password = friendly_password_generator.generate(length=16)
print("Generated User-Friendly Password:", password)

# Create an instance of Passphrase
passphrase_generator = Passphrase()

# Generate a passphrase of length 20 (characters)
passphrase = passphrase_generator.generate(password_length=20)
print("Generated Passphrase:", passphrase)
```

## API Reference

### Classes

- **UserFriendlyPassword**
    - **generate(length: int) -> str**: Generates a user-friendly password of the specified length.

- **Passphrase**
    - **generate(password_length: int) -> str**: Generates a user-friendly passphrase composed of random words.

### Customization Options
- Adjust the number of special characters and digits by modifying `char_amount` and `num_amount` attributes.
- Set minimum and maximum password lengths using `set_min_length` and `set_max_length`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
