import peewee as pw
from src.roastbackup import roastplanmodels as rpm
import bcrypt as bc
from loguru import logger
logger.add('user_log.log', rotation="00:00")


class UserCollection:
    """
    Contains a collection of Users objects
    """
    def __init__(self):
        self.database = rpm.Users

    def add_user(self, user_id, user_alias, user_name, user_last_name, user_email, user_company_name, user_password):
        try:
            self.database.create(
                user_id=user_id,
                user_alias=user_alias,
                user_name=user_name,
                user_last_name=user_last_name,
                user_email=user_email,
                user_company_name=user_company_name,
                user_password=self.hash_password(user_password)
            )
            logger.info(f'User added successfully: {user_id}')
            return True
        except pw.IntegrityError:
            logger.warning(f'User {user_id} already exists')
            return False

    @staticmethod
    def hash_password(password):
        """
        Returns a binary hash of password
        :param password: string
        :return: binary
        """
        convert_to_bytes = bytes(password)
        result = bc.hashpw(convert_to_bytes, bc.gensalt())
        return result

    def delete_user(self, user_id):
        """
        Deletes an existing user
        """
        try:
            self.database.get_by_id(user_id).delete_instance()
            logger.info(f'User {user_id} successfully removed')
            return True
        except pw.DoesNotExist:
            logger.warning(f'User {user_id} cannot be deleted - user not found')
            return False

    def modify_user(self, user_id, user_alias, user_name, user_last_name, user_email, user_company_name, user_password):
        try:
            modify = self.database.get_by_id(user_id)
            (modify.update({self.database.user_alias: user_alias,
                            self.database.user_name: user_name,
                            self.database.user_last_name: user_last_name,
                            self.database.user_email: user_email,
                            self.database.user_company_name: user_company_name,
                            self.database.user_password: self.hash_password(user_password)}).
             where(self.database.user_id == user_id).execute())
            logger.info(f'User {user_id} modified')
            return True
        except pw.DoesNotExist:
            logger.warning(f'User {user_id} cannot be modified; User does not exist')
            return False

    def search_user(self, user_id):
        try:
            return_value = self.database.get_by_id(user_id)
            logger.info(f'User {user_id} found')
            return return_value
        except pw.DoesNotExist:
            logger.warning(f'User {user_id} not found')
            return None
