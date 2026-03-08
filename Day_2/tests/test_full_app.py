import unittest

class TestBankingApplication(unittest.TestCase):

    def test_valid_login(self):
        username = "Chaalika26"
        password = "Dedeepya@30"

        self.assertEqual(username, "Chaalika26")
        self.assertEqual(password, "Dedeepya@30")

    def test_invalid_password(self):
        saved_password = "Dedeepya@30"
        entered_password = "wrong123"

        self.assertNotEqual(saved_password, entered_password)

    def test_deposit_addition(self):
        old_balance = 1000
        deposit_amount = 500
        new_balance = old_balance + deposit_amount

        self.assertEqual(new_balance, 1500)

    def test_withdraw_deduction(self):
        old_balance = 1000
        withdraw_amount = 300
        new_balance = old_balance - withdraw_amount

        self.assertEqual(new_balance, 700)

    def test_insufficient_balance(self):
        balance = 200
        withdraw_amount = 500

        self.assertTrue(withdraw_amount > balance)

if __name__ == "__main__":
    unittest.main()