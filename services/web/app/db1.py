import json
import os
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
import hashlib
import pandas as pd
import uuid
import boto3
import botocore

def md5_hash(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()

def generate_unique_id() -> str:
    return str(uuid.uuid4())


class MessageEncoder(json.JSONEncoder):
    """ Encoder class for Message objects. """
    def default(self, obj):
        if isinstance(obj, Message):
            return {
                "is_user": obj.is_user,
                "content": obj.content,
                "creation_date": obj.creation_date,
            }
        return json.JSONEncoder.default(self, obj)

class ChatDecoder(json.JSONDecoder):
    """ Decoder class for Chat objects. """
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if 'messages' in obj:
            user_id = obj.get('user_id', '')
            name = obj.get('name', '')
            model_name = obj.get('model_name', '')
            on_all_documents = obj.get('on_all_documents', True)
            imported_document_hashes = obj.get('imported_document_hashes', [])
            messages = obj.get('messages', [])
            chat_id = obj.get('chat_id', generate_unique_id())

            # Construct Chat object with extracted parameters
            return Chat(user_id, name, model_name, on_all_documents, imported_document_hashes, messages, chat_id)
        
        return obj


class User:
    """
    This class represents an individual user in the system, providing methods to manage and update user data.

    #### Parameters:
        - `user_id (str)`: The unique identifier for the user.
        - `password (str)`: The user's password which will be hashed using MD5.
        - `role (str)`: Optional. Specifies the user's role.
        - `creation_date (str)`: The ISO formatted date and time when the user was created.
        - `is_validated (bool)`: Optional. Wheather the user is validated by admin. 
        - `start (Optional[str])`: Optional. The start date from which the user can access the application.
        - `expire (Optional[str])`: Optional. The expiration date after which the user cannot access the application.
        - `imports (List[str])`: Optional. A list of document hashes that the user has imported.
        - `chat_history (List[str])`: Optional. A list of chat history hashes.

    #### Attributes:
        - `user_id (str)`: User's unique identifier.
        - `password (str)`: Hashed password for the user.
        - `role (str)`: The user's role.
        - `creation_date (str)`: The ISO formatted date and time when the user was created.
        - `is_validated (bool)`: Wheather the user is validated by admin.
        - `start (Optional[str])`: Start date for the user's access.
        - `expire (Optional[str])`: Expiration date for the user's access.
        - `imports (List[str])`: List of imported document IDs.
        - `chat_history (List[str])`: List of chat history entries.

    #### Methods:
        - `update(password, admin, creation_date, is_validated, start, expire, imports, chat_history) -> None`: 
            Updates the user's attributes.
    """
    def __init__(self, user_id: str, password: str, role: str = 'user', 
                 creation_date: str = datetime.now().isoformat(), is_validated: bool = True, start: Optional[str] = None,
                 expire: Optional[str] = None, imports: List[str] = [], chat_history: List[str] = []) -> None:
        """
        ### Waring
        Password must be hashed before creating a User object. You can use `md5_hash(s: str) -> str` or create the user directly with the database as follow: 
        1. `user_db = db.Userdatabase()`
        2. `user_db.create_user("my_id", "my_password")` 
        """
        self.user_id: str = user_id
        if password is not None and len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        self.password: str = password
        self.role: str = role
        self.creation_date: str = creation_date
        self.start: Optional[str] = start
        self.expire: Optional[str] = expire
        self.is_validated = is_validated
        self.imports: List[str] = imports
        self.chat_history: List[str] = chat_history

    def update(self, password: Optional[str] = None, role: Optional[str] = None, is_validated: bool = None, start: Optional[str] = None,
               expire: Optional[str] = None, imports: Optional[List[str]] = None, chat_history: Optional[List[str]] = None) -> None:
        """Update user data. Parameters can be None if not updated. If password updated, it must be at least 8 characters long."""
        if password is not None and len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if password is not None:
            self.password = md5_hash(password)
        if role is not None:
            self.role = role
        if is_validated is not None:
            self.is_validated = is_validated
        if start is not None:
            self.start = start
        if expire is not None:
            self.expire = expire
        if imports is not None:
            self.imports = imports
        if chat_history is not None:
            self.chat_history = chat_history
    def __str__(self) -> str:
        user_info = [
        f"\tUser ID: {self.user_id}",
        f"\tUser password: ****",
        f"\tRole: {self.role}",
        f"\tCreation Date: {self.creation_date}",
        f"\tIs Validated: {self.is_validated}",
        f"\tStart: {self.start}",
        f"\tExpire: {self.expire}",
        f"\tImports: {self.imports}",
        f"\tChat History: {self.chat_history}"
        ]
        return "\n".join(user_info)

class UserDatabase:
    """
    This class manages a database of users stored in a JSON file, providing methods to create, retrieve, update, and delete users.

    #### Parameters:
        - `filename (str)`: The name of the JSON file that stores user data.

    #### Attributes:
        - `filename (str)`: File path to the JSON database.
        - `users (List[User])`: List of User objects representing the users in the database.

    #### Methods:
        - `load_database() -> List[User]`: 
            Loads users from the JSON file, returning a list of User objects.
        - `save_database() -> None`: 
            Saves the current list of users back to the JSON file.
        - `create_user(id: str, password: str, role: str = 'user', start: Optional[str] = None, expire: Optional[str] = None, imports: List[str] = [], chat_history: List[str] = []) -> User`: 
            Creates a new user, adds it to the database and returns it.
        - `add_user(self, Union[User, List[User]]) -> bool`: 
            Adds one or a list of user object(s) directly to the database. Returns whether the user already exist.
        - `get_user_for_login(id: str, password: str) -> Optional[User]`: 
            Retrieves a user by their ID and password if the password matches. Returns None if does not exist.
        - `get_user(id: str) -> Optional[User]`: 
            Retrieves a user by its ID. Returns None if does not exist.
        - `update_user_by_id(id: str, **kwargs) -> User`: 
            Updates a user's details based on provided keyword arguments. Returns the User object if succeful, else None.
        - `update_user(user: User, **kwargs) -> User`: 
            Updates a user's details based on a User object. Returns the User object if succeful, else None.
        - `delete_user_by_id(id: str) -> bool`: 
            Removes a user by their ID from the database. Returns True if the user was found and deleted.
        - `delete_user(users: Union[User, List[User]]) -> bool`: 
            Delete one or a list of user and return True if all users were found and deleted.
        - `to_dataframe(self) -> pd.DataFrame`:
            Converts user list to a pandas DataFrame for admin page.
    """
    def __init__(self, filename: str = 'user_database.json', bucket_name: str = None, dest_dir: str = None) -> None:
        self.filename: str = filename
        self.users: List[User] = self.load_database()
        self.bucket_name = bucket_name
        self.dest_dir = dest_dir


    def load_database(self) -> List[User]:
        """Load the database from a JSON file or create a new one if it does not exist."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    users_data = json.load(file)
                    return [User(**data) for data in users_data]
            else:
                return []
        except IOError as e:
            raise Exception(f"Unable to access the file {self.filename}. Error: {e}")

    def save_database(self) -> None:
        """Save the user database to a JSON file."""
        try:
            with open(self.filename, 'w') as file:
                data = [user.__dict__ for user in self.users]
                json.dump(data, file, indent=4)
            if self.bucket_name is not None:
                s3 = boto3.client('s3')
                if self.dest_dir is None:
                    self.dest_dir = "data/user_database.json"
                with open(self.filename, 'rb') as file:
                    s3.upload_fileobj(file, self.bucket_name, os.path.join("jean-baptiste.trognon@csgroup.eu/", self.dest_dir))
        except IOError as e:
            raise Exception(f"Unable to save the file {self.filename}. Error: {e}")

    def create_user(self, user_id: str, password: str, role: str = 'user', is_validated: bool = True, start: Optional[str] = None,
                    expire: Optional[str] = None, imports: List[str] = [], chat_history: List[str] = []) -> User:
        """Create and add a new user to the database. Password must be at least 8 characters long.
        
        Password will be hashed."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        user = User(user_id, md5_hash(password), role, datetime.now().isoformat(), is_validated, start, expire, imports, chat_history)
        # Check if user with same user_id already exists to avoid duplicates
        if any(existing_user.user_id == user.user_id for existing_user in self.users):
            pass
        else :
            self.users.append(user)
            self.save_database()
        return user
    
    def add_user(self, users: Union[User, List[User]]) -> bool:
        """Adds one or a list of user object(s) directly to the database. Returns whether the user already exists."""
        already_exist = False
        if isinstance(users, User):
            users = [users]  # Convert single user to list containing that user
        for user in users:
            # Check if user with same user_id already exists to avoid duplicates
            if any(existing_user.user_id == user.user_id for existing_user in self.users):
                already_exist = True
            else :
                self.users.append(user)
        self.save_database()
        return already_exist

    def get_user_for_login(self, user_id: str, password: str) -> Optional[User]:
        """Retrieve a user by user_id and password, returning the user object if found AND validated."""
        hashed_password = md5_hash(password)
        for user in self.users:
            if user.user_id == user_id and user.password == hashed_password:
                if user.is_validated:
                    return user
                else:
                    return None
        return None
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieve a user by user_id, returning the user object if found and validated."""
        for user in self.users:
            if user.user_id == user_id:
                if user.is_validated:
                    return user
                else:
                    return None
        return None

    def update_user_by_id(self, user_id: str, **kwargs: Any) -> User:
        """Update user information by user_id and return the user if successful. If password updated, it must be at least 8 characters long."""
        updated_user = None
        for user in self.users:
            if user.user_id == user_id:
                user.update(**kwargs)
                self.save_database()
                updated_user = user
        return updated_user
    
    def update_user(self, user: User, **kwargs: Any) -> User:
        """Update user information by User object or create the user if not existent. If the password is updated, it must be at least 8 characters long."""
        for existing_user in self.users:
            if existing_user.user_id == user.user_id:
                existing_user.update(**kwargs)
                self.save_database()
                return existing_user

        # If user with given user_id does not exist, create new one using the provided User object
        self.create_user(user)  # This already handles saving the database
        return user

    def delete_user_by_id(self, user_id: str) -> bool:
        """Delete a user by user_id and return True if the user was found and deleted."""
        initial_count = len(self.users)
        self.users = [user for user in self.users if user.user_id != user_id]
        self.save_database()
        return len(self.users) < initial_count
    
    def delete_user(self, users: Union[User, List[User]]) -> bool:
        """Delete one or a list of user and return True if all users were found and deleted."""
        if isinstance(users, User):
            users = [users]
        all_user_deleted = True
        for user in users:
            if(not self.delete_user_by_id(user.user_id)):
                all_user_deleted = False
        return all_user_deleted
    
    def to_dataframe(self) -> pd.DataFrame:
        """Converts user list to a pandas DataFrame for admin page."""
        data = [{
            'user_id': user.user_id,
            'role': user.role,
            'creation_date': datetime.strptime(user.creation_date, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y %H:%M"),
            'import_number': len(user.imports),
            'chat_number': len(user.chat_history)
        } for user in self.users]
        return pd.DataFrame(data)

class Message:
    """
    This class represents a message in the chat system.

    #### Attributes:
        - `is_user (bool)`: Indicates if the message is sent by a user.
        - `content (str)`: The content of the message.
        - `creation_date (str)`: The ISO formatted date and time when the message was created.

    #### Methods:
        - `update(content) -> None`: 
            Updates the message content.
    """
    def __init__(self, message: Dict[str, Any]):
        self.is_user: bool = message["is_user"]
        self.content: str = message["content"]
        self.creation_date: str = message["creation_date"]

    def update(self, content: Optional[str] = None) -> None:
        """Update message content."""
        if content is not None:
            self.content = content
    
    def __str__(self) -> str:
        s = "> Model at "
        if(self.is_user):
            s = "> User at "
        s += self.creation_date
        s += ":\n\t" + self.content
        return s

class Chat:
    """
    This class represents a chat room in the system.

    #### Parameters:
        - `user_id (str)`: The unique identifier of the user who created the chat.
        - `name (str)`: The name of the chat room.
        - `model_name (str)`: The name of the chat model used in the chat room.
        - `on_all_documents (bool)`: Specifies whether the model uses all documents in its context or only imported documents.
        - `imported_document_hashes (List[str])`: List of document hashes imported into the chat.

    #### Attributes:
        - `chat_id (str)`: The unique identifier of the chat room.
        - `user_id (str)`: The unique identifier of the user who created the chat.
        - `name (str)`: The name of the chat room.
        - `model_name (str)`: The name of the chat model used in the chat room.
        - `on_all_documents (bool)`: Specifies whether the model uses all documents in its context or only imported documents.
        - `imported_document_hashes (List[str])`: List of document hashes imported into the chat.
        - `messages (List[Message])`: List of messages in the chat.

    #### Methods:
        - `add_message(is_user, content) -> None`: 
            Adds a message to the chat.
        - `update(name, model_name, on_all_documents, imported_document_hashes) -> None`: 
            Updates the chat attributes.
    """
    def __init__(self, user_id: str, name: str, model_name: str,
                 on_all_documents: bool=True, imported_document_hashes: List[str]=[], 
                 messages: List[Dict[str, Any]]=[], chat_id: str=generate_unique_id()):
        self.chat_id = chat_id
        self.user_id: str = user_id
        self.name: str = name
        self.model_name: str = model_name
        self.on_all_documents: bool = on_all_documents
        self.imported_document_hashes: List[str] = imported_document_hashes
        self.messages: List[Message] = [Message(m) for m in messages]

    def add_message(self, is_user: bool, content: str) -> None:
        """Should not be used on the object to avoid forgetting to synchronize. Use the database method instead."""
        message = Message({"is_user": is_user, "content": content, "creation_date": datetime.now().isoformat()})
        self.messages.append(message)

    def update(self, name: Optional[str] = None, model_name: Optional[str] = None,
            on_all_documents: Optional[bool] = None, imported_document_hashes: Optional[List[str]] = None) -> None:
        """Update chat data."""
        if name is not None:
            self.name = name
        if model_name is not None:
            self.model_name = model_name
        if on_all_documents is not None:
            self.on_all_documents = on_all_documents
        if imported_document_hashes is not None:
            self.imported_document_hashes = imported_document_hashes
    
    def __str__(self) -> str:
        s = f'Chat "{self.name}" between user {self.user_id} and {self.model_name} model:\n\n'
        for m in self.messages:
            s += str(m) + "\n"
        return s

class ChatDatabase:
    """
    This class manages a database of chats stored in a JSON file, providing methods to create, retrieve, update, and delete chats.

    #### Parameters:
        - `filename (str)`: The name of the JSON file that stores chat data.

    #### Attributes:
        - `filename (str)`: File path to the JSON database.
        - `chats (List[Chat])`: List of Chat objects representing the chats in the database.

    #### Methods:
        - `load_database() -> List[Chat]`: 
            Loads chats from the JSON file, returning a list of Chat objects.
        - `save_database() -> None`: 
            Saves the current list of chats back to the JSON file.
        - `create_chat(user_id: str, name: str, model_name: str, on_all_documents: bool, imported_document_hashes: List[str]) -> Chat`: 
            Creates a new chat, adds it to the database, and returns it.
        - `add_chat(chat: Chat) -> None`: 
            Adds a new chat object directly to the database.
        - `get_chat(chat_id: str) -> Optional[Chat]`: 
            Retrieves a chat by its ID. Returns None if it does not exist.
        - `add_message_to_chat_by_id(chat_id: str, is_user: bool, content: str) -> bool`: 
            Adds a message to the specified chat based on its ID.
        - `add_message_to_chat(chat: Chat, is_user: bool, content: str) -> bool`: 
            Adds a message to the specified chat.
        - `add_message_to_chat_from_chat_and_message(self, chat: Chat, message: Message) -> bool`:
            Adds a message object to the specified chat.
        - `update_chat_by_id(chat_id: str, **kwargs) -> Chat`: 
            Updates a chat's information based on provided keyword arguments. Returns the Chat object if successful, else None.
        - `update_chat(chat: Chat, **kwargs) -> Chat`: 
            Updates a chat's information based on a Chat object or creates the chat if it does not exist.
        - `delete_chat_by_id(chat_id: str) -> bool`: 
            Removes a chat by its ID from the database. Returns True if the chat was found and deleted.
        - `delete_chat(chat: Chat) -> bool`: 
            Removes a chat from the database. Returns True if the chat was found and deleted.
    """
    def __init__(self, filename: str = 'chat_history.json'):
        self.filename: str = filename
        self.chats: List[Chat] = self.load_database()

    def load_database(self) -> List[Chat]:
        """Load the database from a JSON file or create a new one if it does not exist."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    chats_data = json.load(file, cls=ChatDecoder)
                    return chats_data
            else:
                return []
        except IOError as e:
            raise Exception(f"Unable to access the file {self.filename}. Error: {e}")

    def save_database(self) -> None:
        """Save the chat database to a JSON file."""
        try:
            with open(self.filename, 'w') as file:
                json.dump([chat.__dict__ for chat in self.chats], file, indent=4, cls=MessageEncoder)
        except IOError as e:
            raise Exception(f"Unable to save the file {self.filename}. Error: {e}")

    def create_chat(self, user_id: str, name: str, model_name: str, on_all_documents: bool=True, 
                    imported_document_hashes: List[str]=[]) -> Chat:
        """Create and add a new chat to the database."""
        chat = Chat(user_id, name, model_name, on_all_documents, imported_document_hashes)
        self.chats.append(chat)
        self.save_database()
        return chat
    
    def add_chat(self, chat: Chat) -> None:
        """Adds a new chat object directly to the database. Returns whether the document already exists."""
        # Check if chat with same chat_id already exists to avoid duplicates
        if any(existing_chat.chat_id == chat.chat_id for existing_chat in self.chats):
            return False
        else:
            self.chats.append(chat)
            self.save_database()
            return True

    def get_chat(self, chat_id: str) -> Optional[Chat]:
        for chat in self.chats:
            if chat.chat_id == chat_id:
                return chat
        return None

    def add_message_to_chat_by_id(self, chat_id: str, is_user: bool, content: str) -> bool:
        """ Adds a message to the specified chat based on its ID. """
        chat = self.get_chat(chat_id)
        if chat:
            chat.add_message(is_user, content)
            self.save_database()
            return True
        return False

    def add_message_to_chat(self, chat: Chat, is_user: bool, content: str) -> bool:
        """ Adds a message to the specified chat. """
        return self.add_message_to_chat_by_id(chat.chat_id, is_user, content)
    
    def add_message_to_chat_from_chat_and_message(self, chat: Chat, message: Message) -> bool:
        """ Adds a message object to the specified chat. """
        return self.add_message_to_chat_by_id(chat.chat_id, message.is_user, message.content)

    def update_chat_by_id(self, chat_id: str, **kwargs: Any) -> Chat:
        """ Update chat information by chat_id and return the chat if successful."""
        updated_chat = None
        for chat in self.chats:
            if chat.chat_id == chat_id:
                chat.update(**kwargs)
                self.save_database()
                updated_chat = chat
        return updated_chat
    
    def update_chat(self, chat: Chat, **kwargs: Any) -> Chat:
        """ Update chat information by Chat object or create the chat if not existent. """
        for existing_chat in self.chats:
            if existing_chat.chat_id == chat.chat_id:
                existing_chat.update(**kwargs)
                self.save_database()
                return existing_chat

        # If chat with given chat_id does not exist, create new one using the provided Chat object
        self.create_chat(chat)  # This already handles saving the database
        return chat

    def delete_chat_by_id(self, chat_id: str) -> bool:
        """Delete a chat by chat_id and return True if the chat was found and deleted."""
        initial_count = len(self.chats)
        self.chats = [chat for chat in self.chats if chat.chat_id != chat_id]
        self.save_database()
        return len(self.chats) < initial_count
    
    def delete_chat(self, chat: Chat) -> bool:
        """Delete a chat and return True if the chat was found and deleted."""
        return self.delete_chat(chat.chat_id)
    

def login(user_id: str, password: str, filename: str = 'user_database.json') -> Optional[User]:
    """Returns the user if it exists and is validated, else returns None"""
    user_db = UserDatabase(filename)
    user = user_db.get_user_for_login(user_id, password)
    del user_db
    return user

def init_database_from_bucket(source_path: str, dest_path: str, bucket_name: str) -> None:
    """Download the user_database JSON file from S3 bucket to dest_path in local. Path is the path of the object."""
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, source_path, dest_path)
        print("Documents successfully imported from S3 to local.")
    except botocore.exceptions.ClientError as e:
        print(f"No such file in S3. source_path: {source_path}, dest_path: {dest_path}, bucket_name: {bucket_name}\nBoto3 error: {e}")  # When source path does not exist