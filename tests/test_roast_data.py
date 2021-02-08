from unittest import TestCase
import peewee as pw
import roastplanmodels as rpm
import mock
import bcrypt
from Users import UserCollection
from RoastDataInformation import RoastDataCollection
from pathlib import Path

test_data = {'Bob': ['bob123', 'burger_bob', 'Bob', 'Belcher', 'bob123@gmail.com', 'Bob\'s Burgers LLC',
                     b'I love hamburgers'],
             'Linda': ['linda123', 'burger_wife', 'Linda', 'Belcher', 'linda@gmail.com', 'Bob\'s Burgers LLC',
                       b'I love bob'],
             'Gene': ['gene234', 'music_genius', 'Gene', 'Belcher', 'gene@gmail.com', 'Gene\'s Musical Soundscape LLC',
                      b'pocket tater-tots are totally a thing'],
             'Tina': ['tina345', 'erotic_friend_fiction_lover', 'Tina', 'Belcher', 'tina@gmail.com',
                      'Erotic Friends and More LLC', b'Jimmy Pesto is the greatest tease']}

roast_data = {1: ['bob123_001', 'bob123', 'e5b844cc57f57094ea4585e235f36c78c1cd222262bb89d53c94dcb4d6b3e55d',
                  'testfile.file', 'test_bucket_001'],
              2: ['linda123_001', 'linda123', 'e5b844cc57f57094ea4185e235f36c78c1cd222262bb89d53c94dcb4d6b3e55d',
                  'testfile.file', 'test_bucket_002'],
              3: ['gene234_001', 'gene234', 'e5b844cc57f57094ea4585e2e5f36c78c1cd222262bb89d53c94dcb4d6b3e55d',
                  'testfile.file', 'test_bucket_003'],
              4: ['tina345_001', 'tina345', 'e5b844cc57f57094ea4585e235f36c74c1cd222262bb89d53c94dcb4d6b3e55d',
                  'testfile.file', 'test_bucket_002']
              }


class TestUserCollection(TestCase):

    def setUp(self):
        """
        Establishes DB connection for setup
        """
        self.db = rpm.db
        self.db.connect(reuse_if_open=True)

    def tearDown(self):
        """
        Drops tables & closes db connection for teardown
        """
        if self.db.table_exists('users'):
            self.db.drop_tables(rpm.Users)
        if self.db.table_exists('roastdata'):
            self.db.drop_tables(rpm.RoastDataInformation)
        self.db.close()

    def test_user_table(self):
        rpm.main()
        correct_columns = ['user_id', 'user_alias', 'user_name', 'user_last_name', 'user_email', 'user_company_name',
                           'user_password']
        test_cols = [x[0] for x in self.db.get_columns('users')]
        primary_key = self.db.get_primary_keys('users')[0]
        assert test_cols == correct_columns
        assert 'user_id' == primary_key

    def test_roastdata_table(self):
        """
        Test that roast plan info table created correctly
        """
        correct_columns = ['data_id', 'user_id', 'data_upload_time', 'data_hash_value', 'data_file_name',
                           'data_bucket_name']
        test_cols = [x[0] for x in self.db.get_columns('roastdata')]
        primary_key = self.db.get_primary_keys('roastdata')[0]
        foreign_key = self.db.get_foreign_keys('roastdata')[0][0]
        assert test_cols == correct_columns
        assert 'data_id' == primary_key
        assert 'user_id' == foreign_key

    def test_create_tables(self):
        """
        Tests that create_table function works as expected
        """
        result = rpm.create_tables(self.db, (rpm.Users, rpm.RoastDataInformation))
        assert result
        assert self.db.table_exists('users')
        assert self.db.table_exists('roastdata')

    def test_main(self):
        """
        Tests that main function works as expected
        """
        with mock.patch('roastplanmodels.create_tables') as ct:
            result = rpm.main()
            assert result
        ct.assert_called_with(rpm.db, (rpm.Users, rpm.RoastDataInformation))


class UsersTests(TestCase):
    def setUp(self):
        """
        Establishes DB connection for setup
        """
        self.db = pw.SqliteDatabase(':memory:')
        rpm.main()
        self.users = UserCollection()

    def tearDown(self):
        """
        Drops tables & closes db connection for teardown
        """
        self.db.drop_tables((rpm.Users, rpm.RoastDataInformation))
        self.db.close()

    def test_user_collection_init(self):
        """
        Tests that a user collection object can be instant
        """
        self.assertEqual(self.users.database, rpm.Users)
        self.assertIsInstance(self.users, UserCollection)

    def test_add_user(self):
        """
        Tests that add_user function works properly
        """
        user1 = self.users.add_user(test_data['Bob'][0], test_data['Bob'][1], test_data['Bob'][2], test_data['Bob'][3],
                                    test_data['Bob'][4], test_data['Bob'][5], test_data['Bob'][6])
        self.assertTrue(user1)
        self.assertEqual(self.users.database.get_by_id(test_data['Bob'][0]).user_id, test_data['Bob'][0])

        same_user = self.users.add_user(test_data['Bob'][0], test_data['Bob'][1], test_data['Bob'][2],
                                        test_data['Bob'][3], test_data['Bob'][4], test_data['Bob'][5],
                                        test_data['Bob'][6])
        self.assertFalse(same_user)
        second_user = self.users.add_user(test_data['Linda'][0], test_data['Linda'][1], test_data['Linda'][2],
                                          test_data['Linda'][3], test_data['Linda'][4], test_data['Linda'][5],
                                          test_data['Linda'][6])
        self.assertTrue(second_user)
        self.assertEqual(self.users.database.get_by_id(test_data['Linda'][0]).user_id, test_data['Linda'][0])

    def test_password_hashes_correctly_and_returns_hash(self):
        """
        Tests password hashing for users
        """
        user1_password = test_data['Bob'][6]
        user2_password = test_data['Gene'][6]
        hashed1 = self.users.hash_password(user1_password)
        hashed2 = self.users.hash_password(user2_password)
        self.assertTrue(bcrypt.checkpw(user1_password, hashed1))
        self.assertTrue(bcrypt.checkpw(user2_password, hashed2))

    def test_delete_user(self):
        self.assertFalse(self.users.delete_user(test_data['Gene'][0]))
        self.users.add_user(test_data['Bob'][0], test_data['Bob'][1], test_data['Bob'][2], test_data['Bob'][3],
                            test_data['Bob'][4], test_data['Bob'][5], test_data['Bob'][6])
        delete_user = self.users.delete_user(test_data['Bob'][0])
        self.assertTrue(delete_user)
        with self.assertRaises(pw.DoesNotExist):
            self.users.database.get_by_id('bob123')

    def test_modify_user(self):
        self.assertFalse(self.users.modify_user(
            test_data['Bob'][0], test_data['Bob'][1], test_data['Bob'][2], test_data['Bob'][3],
            test_data['Bob'][4], test_data['Bob'][5], test_data['Bob'][6]
        ))
        self.users.add_user(
            test_data['Bob'][0], test_data['Bob'][1], test_data['Bob'][2], test_data['Bob'][3],
            test_data['Bob'][4], test_data['Bob'][5], test_data['Bob'][6]
        )
        changed_user = self.users.modify_user(
            test_data['Bob'][0], test_data['Gene'][1], test_data['Linda'][2], test_data['Tina'][3],
            test_data['Tina'][4], test_data['Gene'][5], test_data['Bob'][6]
        )
        self.assertTrue(changed_user)
        bob_data = self.users.database['bob123']
        self.assertEqual(bob_data.user_email, test_data['Tina'][4])
        self.assertEqual(bob_data.user_alias, test_data['Gene'][1])
        self.assertEqual(bob_data.user_name, test_data['Linda'][2])
        self.assertEqual(bob_data.user_company_name, test_data['Gene'][5])

    def test_search_user(self):
        """
        Test that user collection returns correct user
        """
        self.users.add_user(
            test_data['Bob'][0], test_data['Bob'][1], test_data['Bob'][2], test_data['Bob'][3],
            test_data['Bob'][4], test_data['Bob'][5], test_data['Bob'][6]
        )
        not_in_db = self.users.search_user(test_data['Tina'][0])
        self.assertEqual(not_in_db, None)
        self.assertEqual(self.users.search_user(test_data['Bob'][0]),
                         self.users.database['bob123'])


class RoastDataInformationTests(TestCase):
    def setUp(self):
        self.db = pw.SqliteDatabase(':memory:')
        rpm.main()
        self.roasting_data = RoastDataCollection()
        self.users = UserCollection()
        self.users.add_user(
            test_data['Bob'][0], test_data['Bob'][1], test_data['Bob'][2], test_data['Bob'][3],
            test_data['Bob'][4], test_data['Bob'][5], test_data['Bob'][6]
        )

    def tearDown(self):
        self.db.drop_tables((rpm.Users, rpm.RoastDataInformation))
        self.db.close()

    def test_roast_data_collection_init(self):
        """
        Tests that roast data collection is created
        """
        self.assertEqual(self.roasting_data.database, rpm.RoastDataInformation)
        self.assertIsInstance(self.roasting_data, RoastDataCollection)

    def test_add_roasting_data_information(self):
        """
        Tests that roast data file information is added to db
        """
        first_file_data = self.roasting_data.add_roast_data_information(roast_data[1][0], roast_data[1][1],
                                                                        roast_data[1][2], roast_data[1][3],
                                                                        roast_data[1][4])
        self.assertTrue(first_file_data)
        self.assertEqual(self.roasting_data.database.get_by_id(roast_data[1][0]).data_id, roast_data[1][0])

        same_data = self.roasting_data.add_roast_data_information(
            roast_data[1][0], roast_data[1][1], roast_data[1][2],
            roast_data[1][3], roast_data[1][4]
        )

        self.assertFalse(same_data)
        second_file_data = self.roasting_data.add_roast_data_information(
            roast_data[2][0], roast_data[2][1], roast_data[2][2],
            roast_data[2][3], roast_data[2][4]
        )
        self.assertTrue(second_file_data)
        self.assertEqual(self.roasting_data.database.get_by_id(roast_data[2][0]).data_id, roast_data[2][0])

    def test_delete_roast_data_information(self):
        self.assertFalse(self.roasting_data.delete_roast_data_information(roast_data[3][0]))
        self.roasting_data.add_roast_data_information(
            roast_data[1][0], roast_data[1][1], roast_data[1][2],
            roast_data[1][3], roast_data[1][4]
        )
        delete_data = self.roasting_data.delete_roast_data_information(roast_data[1][0])
        self.assertTrue(delete_data)
        with self.assertRaises(pw.DoesNotExist):
            self.roasting_data.database.get_by_id('bob123_001')

    def test_modifies_roast_data_information(self):
        self.assertFalse(self.roasting_data.modify_roast_data_information(
            roast_data[1][0], roast_data[1][1], roast_data[1][2],
            roast_data[1][3], roast_data[1][4]
        ))
        self.roasting_data.add_roast_data_information(
            roast_data[1][0], roast_data[1][1], roast_data[1][2],
            roast_data[1][3], roast_data[1][4]
        )
        changed_data = self.roasting_data.modify_roast_data_information(
            roast_data[1][0], roast_data[1][1], roast_data[3][2],
            roast_data[4][3], roast_data[2][4]
        )
        self.assertTrue(changed_data)
        changed_data = self.roasting_data.database.get_by_id(roast_data[1][0])
        self.assertEqual(changed_data.user_id.user_id, roast_data[1][1])
        self.assertEqual(changed_data.data_id, roast_data[1][0])
        self.assertEqual(changed_data.data_hash_value, roast_data[3][2])
        self.assertEqual(changed_data.data_file_name, roast_data[4][3])
        self.assertEqual(changed_data.data_bucket_name, roast_data[2][4])

    def test_get_file_hash_returns_correct_hash(self):
        path = Path(__file__).parent / 'testfile.file'
        return_value = self.roasting_data.get_file_hash(path)
        self.assertEqual(return_value, 'e5b844cc57f57094ea4585e235f36c78c1cd222262bb89d53c94dcb4d6b3e55d')

    def test_search_roast_data_information_returns_correct_data(self):
        self.roasting_data.add_roast_data_information(
            roast_data[1][0], roast_data[1][1], roast_data[1][2],
            roast_data[1][3], roast_data[1][4]
        )
        not_in_db = self.roasting_data.search_roast_data_information(roast_data[4][0])
        self.assertEqual(not_in_db, None)
        self.assertEqual(self.roasting_data.search_roast_data_information(roast_data[1][0]),
                         self.roasting_data.database.get_by_id(roast_data[1][0]))

    def test_get_all_data_by_user_returns_roast_information(self):
        self.roasting_data.add_roast_data_information(
            roast_data[1][0], roast_data[1][1], roast_data[1][2],
            roast_data[1][3], roast_data[1][4]
        )
        not_in_db = self.roasting_data.get_all_data_by_user('does_not_exist')
        self.assertEqual(not_in_db, None)
        self.assertEqual(
            self.roasting_data.get_all_data_by_user(test_data['Bob'][0]),
            roast_data[1]
        )
