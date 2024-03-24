"""Тесты аккаунта."""

import unittest
from src.entities.account_data import AccountData  # pylint:disable=E0401
# from src.db.data_base_sqlite import SQLite  # pylint:disable=E0401
# from src.utils.utils_consts import ConstDB, ConstCore  # pylint:disable=E0401


# если будем ожидать неудачу от тестов
# @unittest.expectedFailure
class TestAccount(unittest.TestCase):
    """Tests"""

    def setUp(self):
        # создание сущностей аккаунтов
        self.acc_empty = AccountData(username="", password="", data=[])
        self.acc_new_user = AccountData(
            username="Vovqa", password="123456", data=[])

        # примерный вид листа для обновления данных пользователя
        self.data_for_new_user = [
            ["Steam", "666Vovqa666", "SteamPass123"],
            ["VK", "111Vovqa111", "123passVk"]
        ]

        # создание мока sqlite
        # self.sql_mock = SQLite(":memory:", log_level=ConstDB.LOG_1_OFF.value)
        # создаём таблицу аккаунтов если её нету:
        # SQLite.exec_query(self.__sql_connect_account,
                        #   ConstCore.NEW_TABLE_ACCOUNTS.value)

    def test_acc_is_empty(self):
        """test"""
        self.assertEqual(self.acc_empty.get_user_name(), "")
        self.assertEqual(self.acc_empty.get_user_pass(), "")
        self.assertEqual(self.acc_empty.get_user_data(), [])

    def test_update_data(self):
        """test"""
        self.acc_new_user.set_user_data(self.data_for_new_user)
        # проверяем нужный нам индекс на совпадение
        index = 0
        # equal
        self.assertEqual(self.acc_new_user.get_user_name(), "Vovqa")
        self.assertEqual(self.acc_new_user.get_user_pass(), "123456")
        self.assertEqual(self.acc_new_user.get_user_data()[index][index],
                         self.data_for_new_user[index][index])
        self.assertListEqual(
            self.acc_new_user.get_user_data(),
            self.data_for_new_user)
        self.assertListEqual(
            self.acc_new_user.get_user_data()[0],
            self.data_for_new_user[0])
