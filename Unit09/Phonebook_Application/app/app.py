"""PhoneBook Application that saves files and implements basic Auth using hashed password"""

import csv
from dataclasses import dataclass, asdict
from typing import Dict, List
import os
import hashlib

COUNTRY_CODES: Dict[str, str] = {
    # --- North America ---
    "+1": "USA/Canada",
    "+1242": "Bahamas",
    "+1246": "Barbados",
    "+1264": "Anguilla",
    "+1268": "Antigua and Barbuda",
    "+1284": "British Virgin Islands",
    "+1345": "Cayman Islands",
    "+1441": "Bermuda",
    "+1473": "Grenada",
    "+1649": "Turks and Caicos",
    "+1664": "Montserrat",
    "+1721": "Sint Maarten",
    "+1758": "Saint Lucia",
    "+1767": "Dominica",
    "+1784": "Saint Vincent & Grenadines",
    "+1849": "Dominican Republic",
    "+1868": "Trinidad and Tobago",
    "+1869": "Saint Kitts and Nevis",
    "+1876": "Jamaica",
    "+1939": "Puerto Rico",
    # --- Europe ---
    "+44": "UK",
    "+33": "France",
    "+49": "Germany",
    "+39": "Italy",
    "+34": "Spain",
    "+351": "Portugal",
    "+352": "Luxembourg",
    "+353": "Ireland",
    "+31": "Netherlands",
    "+32": "Belgium",
    "+41": "Switzerland",
    "+43": "Austria",
    "+46": "Sweden",
    "+47": "Norway",
    "+45": "Denmark",
    "+358": "Finland",
    "+30": "Greece",
    "+48": "Poland",
    "+420": "Czech Republic",
    "+36": "Hungary",
    "+40": "Romania",
    "+359": "Bulgaria",
    "+385": "Croatia",
    "+381": "Serbia",
    "+386": "Slovenia",
    "+421": "Slovakia",
    "+370": "Lithuania",
    "+371": "Latvia",
    "+372": "Estonia",
    "+7": "Russia/Kazakhstan",
    "+380": "Ukraine",
    "+90": "Turkey",
    # --- Asia & Oceania ---
    "+86": "China",
    "+91": "India",
    "+81": "Japan",
    "+82": "South Korea",
    "+61": "Australia",
    "+64": "New Zealand",
    "+62": "Indonesia",
    "+63": "Philippines",
    "+65": "Singapore",
    "+66": "Thailand",
    "+84": "Vietnam",
    "+60": "Malaysia",
    "+886": "Taiwan",
    "+852": "Hong Kong",
    "+92": "Pakistan",
    "+94": "Sri Lanka",
    "+880": "Bangladesh",
    "+977": "Nepal",
    "+95": "Myanmar",
    # --- Middle East ---
    "+971": "UAE",
    "+966": "Saudi Arabia",
    "+972": "Israel",
    "+98": "Iran",
    "+964": "Iraq",
    "+974": "Qatar",
    "+965": "Kuwait",
    "+968": "Oman",
    "+962": "Jordan",
    "+961": "Lebanon",
    # --- Africa ---
    "+20": "Egypt",
    "+27": "South Africa",
    "+234": "Nigeria",
    "+254": "Kenya",
    "+212": "Morocco",
    "+213": "Algeria",
    "+216": "Tunisia",
    "+251": "Ethiopia",
    "+233": "Ghana",
    "+225": "Ivory Coast",
    "+255": "Tanzania",
    "+256": "Uganda",
    "+260": "Zambia",
    "+263": "Zimbabwe",
    # --- South America ---
    "+55": "Brazil",
    "+54": "Argentina",
    "+57": "Colombia",
    "+56": "Chile",
    "+51": "Peru",
    "+58": "Venezuela",
    "+593": "Ecuador",
    "+591": "Bolivia",
    "+595": "Paraguay",
    "+598": "Uruguay",
    # --- Central America ---
    "+52": "Mexico",
    "+507": "Panama",
    "+506": "Costa Rica",
    "+503": "El Salvador",
    "+502": "Guatemala",
    "+504": "Honduras",
    "+505": "Nicaragua",
}

VALID_CATEGORIES = ["General", "Family", "Friends", "Emergency", "Favourites"]


@dataclass
class Contact:
    """
    Represents a single contact in the phonebook.

    This class automatically handles data validation and normalization:
    - Calculates the 'country' based on the phone prefix.
    - Defaults 'category' to 'General' if an invalid one is provided.
    """
    name: str
    phone: str
    email: str
    country: str = "Unknown"
    category: str = "General"

    def __post_init__(self):
        """
        Runs automatically after initialization to normalize data.
        """
        if self.country == "Unknown":
            self.country = self._calculate_country()

        if self.category not in VALID_CATEGORIES:
            self.category = "General"

    def _calculate_country(self) -> str:
        """Determines country name by matching phone prefix against known codes."""
        sorted_codes = sorted(COUNTRY_CODES.keys(), key=len, reverse=True)
        for code in sorted_codes:
            if self.phone.startswith(code):
                return COUNTRY_CODES[code]
        return "Unknown"

    def update_phone(self, new_phone: str):
        """
        Updates the phone number and forces a recalculation of the country.
        
        This prevents 'stale data' where a phone number changes but the 
        country field remains the old value.
        """
        self.phone = new_phone
        self.country = self._calculate_country()


@dataclass
class User:
    """
    Represents a system user. 
    Stores the password as a secure hash and never as plain text password.
    """
    username: str
    password_hash: str

    def verify_password(self, input_password: str) -> bool:
        """
        Hashes the input password and compares it to the stored hash.
        Returns True if they match.
        """
        encoded_input = input_password.encode()
        input_hash = hashlib.sha256(encoded_input).hexdigest()
        return input_hash == self.password_hash


class Authenticator:
    """
    Manages the security context of the application.
    Handles user registration (setup), login, and session state.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.current_user: User = None

    def setup_account(self, username: str, raw_password: str):
        """Creates a new user, hashes their password, and saves to CSV."""
        encoded = raw_password.encode()
        hashed = hashlib.sha256(encoded).hexdigest()

        self.current_user = User(username, hashed)
        self._save_to_csv()

    def login(self, raw_password: str) -> bool:
        """
        Attempts to log the user in.
        Loads data from disk if necessary and verifies credentials.
        """
        if not self.current_user:
            self._load_from_csv()

        if self.current_user and self.current_user.verify_password(raw_password):
            return True
        else:
            return False

    def _save_to_csv(self):
        """Persists the current user credentials to disk."""
        with open(self.filename, mode="w", encoding="UTF-8") as file:
            fieldnames = ["username", "password_hash"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(asdict(self.current_user))

    def _load_from_csv(self):
        """Loads user credentials from disk into memory."""
        if not os.path.exists(self.filename):
            return

        with open(self.filename, mode="r", encoding="UTF-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # We only support one user, so we load the first row and stop.
                self.current_user = User(**row)
                break


class Phonebook:
    """
    The Controller for contact data.
    
    Manages the lifecycle (CRUD) of contacts and handles 
    persistence to the CSV file.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.contacts: List[Contact] = []
        self.load_contacts()

    def add_contact(self, contact: Contact):
        """Adds a new contact to the list and saves immediately."""
        self.contacts.append(contact)
        self.save_contacts()

    def search_contacts(self, query: str) -> List[Contact]:
        """
        Returns a list of contacts where the name matches the query.
        The search is case-insensitive.
        """
        results = []
        for contact in self.contacts:
            if query.lower() in contact.name.lower():
                results.append(contact)
        return results

    def delete_contact(self, contact: Contact):
        """Removes a specific contact object from the list and updates the file."""
        if contact in self.contacts:
            self.contacts.remove(contact)
            self.save_contacts()

    def save_contacts(self):
        """Writes the current list of contacts to the CSV file."""
        with open(self.filename, mode="w", newline="", encoding="UTF-8") as file:
            fieldnames = ["name", "phone", "country", "email", "category"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow(asdict(contact))

    def load_contacts(self):
        """Reads contacts from the CSV file into memory."""
        if not os.path.exists(self.filename):
            return

        with open(self.filename, mode="r", encoding="UTF-8") as file:
            reader = csv.DictReader(file)
            for line in reader:
                self.contacts.append(Contact(**line))


def attempt_login(auth: Authenticator) -> bool:
    """
    Handles the UI flow for authentication.
    
    Determines if the user needs to Register (Setup) or Login
    based on the existence of the credentials file.
    """
    if os.path.exists(auth.filename):
        print("Login Required")
        password = input("Please enter your password: ")
        return auth.login(raw_password=password)
    else:
        print("No account found. Starting setup...")
        username = input("Please enter new username: ")
        password = input("Please enter new password: ")
        auth.setup_account(username=username, raw_password=password)
        return True


def add_contact(phonebook: Phonebook):
    """
    UI handler for creating a new contact.
    Includes validation loop for the Category field.
    """
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email: ")

    category = "General"

    # Input validation loop
    while True:
        print(f"Options: {' | '.join(VALID_CATEGORIES)}")
        category_input = input("Category (Press Enter for 'General'): ").strip().title()

        if not category_input:
            category = "General"
            break

        if category_input in VALID_CATEGORIES:
            category = category_input
            break

        print(f"'{category_input}' is not valid. Please choose from the list.")

    contact = Contact(name, phone, email, category=category)
    phonebook.add_contact(contact)
    print("Contact saved!")


def search_contact(phonebook: Phonebook):
    """UI handler for searching and displaying results."""
    query = input("Enter name to search: ").strip()
    matches = phonebook.search_contacts(query)

    if not matches:
        print("No contacts found.")
        return

    print(f"\nFound {len(matches)} result(s)")
    for contact in matches:
        print(f" - {contact.name} ({contact.phone}) [{contact.category}]")


def handle_list_contacts(phonebook: Phonebook):
    """UI handler to list all contacts sorted by name."""
    print("\n--- All Contacts ---")

    sorted_contacts = sorted(phonebook.contacts, key=lambda c: c.name)

    if not sorted_contacts:
        print("Phonebook is empty.")
        return

    for c in sorted_contacts:
        print(f" - {c.name} | {c.phone} ({c.country}) | {c.category}")


def handle_update_contact(phonebook: Phonebook):
    """
    UI handler for modifying an existing contact.
    Ensures 'update_phone' is called when changing numbers to keep data consistent.
    """
    print("\n--- Update Contact ---")
    query = input("Enter name to search: ").strip()
    matches = phonebook.search_contacts(query)

    if not matches:
        print("No contact found.")
        return

    target = matches[0]
    print(f"Editing: {target.name} | {target.phone}")

    print("1. Name")
    print("2. Phone")
    print("3. Email")
    choice = input("Select: ")

    if choice == "1":
        target.name = input("Enter new name: ")
    elif choice == "2":
        new_phone = input("Enter new phone: ")
        target.update_phone(new_phone)
        print(f"Country updated to: {target.country}")
    elif choice == "3":
        target.email = input("Enter new email: ")

    phonebook.save_contacts()
    print("Contact updated!")


def handle_delete_contact(phonebook: Phonebook):
    """UI handler for deleting a contact with a confirmation prompt."""
    print("\n--- Delete Contact ---")
    query = input("Enter name to delete: ").strip()
    matches = phonebook.search_contacts(query)

    if not matches:
        print("No contact found")
        return

    target = matches[0]
    print(f"Found: {target.name} | {target.phone} | {target.country}")

    confirm = input("Are you sure you want to delete this contact? (y/n)?: ").lower()

    if confirm == "y":
        phonebook.delete_contact(target)
        print("Contact deleted permanently")
    else:
        print("Deletion Cancelled")


def main():
    """
    Application Entry Point.
    1. Handles Authentication.
    2. Enters Main Event Loop.
    """
    auth = Authenticator("credentials.csv")

    if not attempt_login(auth):
        print("Login failed. Exiting.")
        return

    phonebook = Phonebook("contacts.csv")
    print(f"Welcome, {auth.current_user.username}!")

    while True:
        print("\n--- MENU ---")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. View All")
        print("4. Update a contact")
        print("5. Delete a contact")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            add_contact(phonebook)
        elif choice == "2":
            search_contact(phonebook)
        elif choice == "3":
            handle_list_contacts(phonebook)
        elif choice == "4":
            handle_update_contact(phonebook)
        elif choice == "5":
            handle_delete_contact(phonebook)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
