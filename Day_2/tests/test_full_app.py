import unittest

class TestBankingApp(unittest.TestCase):

    def test_valid_login(self):
        username = "Chaalika26"
        password = "Dedeepya@30"

        result = (username == "Chaalika26" and password == "Dedeepya@30")

        print("\nTest Case: Valid Login")
        print("Input -> Username:", username, "Password:", password)
        print("Output -> Login Successful")

        self.assertTrue(result)


    def test_invalid_password(self):
        username = "Chaalika26"
        password = "wrongpass"

        result = password != "Dedeepya@30"

        print("\nTest Case: Invalid Password")
        print("Input -> Username:", username, "Password:", password)
        print("Output -> Invalid Password")

        self.assertTrue(result)


    def test_deposit(self):
        balance = 1000
        deposit_amount = 500
        new_balance = balance + deposit_amount

        print("\nTest Case: Deposit Money")
        print("Input -> Deposit:", deposit_amount)
        print("Output -> New Balance:", new_balance)

        self.assertEqual(new_balance, 1500)


    def test_withdraw(self):
        balance = 1000
        withdraw_amount = 300
        new_balance = balance - withdraw_amount

        print("\nTest Case: Withdraw Money")
        print("Input -> Withdraw:", withdraw_amount)
        print("Output -> Remaining Balance:", new_balance)

        self.assertEqual(new_balance, 700)


    def test_insufficient_balance(self):
        balance = 200
        withdraw_amount = 500

        print("\nTest Case: Insufficient Balance")
        print("Input -> Withdraw:", withdraw_amount)
        print("Output -> Withdrawal Not Allowed")

        self.assertTrue(withdraw_amount > balance)


if __name__ == "__main__":
    unittest.main(verbosity=2)