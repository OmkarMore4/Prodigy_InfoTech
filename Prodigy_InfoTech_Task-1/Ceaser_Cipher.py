def caesar_cipher(text, shift, encrypt=True):
    result = ""
    if not encrypt:
        shift = -shift  # Reverse shift for decryption

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result


def main():
    while True:
        print("\nCaesar Cipher Program")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1' or choice == '2':
            text = input("Enter the message: ")
            shift = int(input("Enter the shift value: "))
            encrypt = choice == '1'
            result = caesar_cipher(text, shift, encrypt)
            print(f"\nResult: {result}\n")

        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
