import unittest

from sturdy import resolve


# TODO: add guards


@unittest.skip("refactoring")
class TestSimpleTransactionActionFactory(unittest.TestCase):
    def setUp(self) -> None:
        resolve("Plugin.Load", "sturdy.extras.empty_command")()
        resolve("Plugin.Load", "sturdy.extras.simple_transaction")()
        resolve("Plugin.Load", "tests.mocks.plugins.balance_transfer")()

    def test_create_action_single_command(self):
        alice = resolve("BalanceTransfer.CreateAccount", 100)
        bob = resolve("BalanceTransfer.CreateAccount", 100)
        transfer = resolve("BalanceTransfer.CreateTransferInfo", alice, bob, 100)

        cmd_do = resolve(
            "BalanceTransfer.ChangeBalanceCommand", transfer.sender, -transfer.value
        )

        cmd_tuple = (cmd_do,)

        action = resolve("SimpleTransaction.CreateAction", cmd_tuple)

        action.do()
        self.assertEqual(0, alice.current_balance)

        action.undo()
        self.assertEqual(0, alice.current_balance)

    def test_create_action_single_command_tuple(self):
        alice = resolve("BalanceTransfer.CreateAccount", 100)
        bob = resolve("BalanceTransfer.CreateAccount", 100)
        transfer = resolve("BalanceTransfer.CreateTransferInfo", alice, bob, 100)

        cmd_do = resolve(
            "BalanceTransfer.ChangeBalanceCommand", transfer.sender, -transfer.value
        )

        action = resolve("SimpleTransaction.CreateAction", cmd_do)

        action.do()
        self.assertEqual(0, alice.current_balance)

        action.undo()
        self.assertEqual(0, alice.current_balance)

    def test_create_action_do_and_undo_command(self):
        alice = resolve("BalanceTransfer.CreateAccount", 100)
        bob = resolve("BalanceTransfer.CreateAccount", 100)
        transfer = resolve("BalanceTransfer.CreateTransferInfo", alice, bob, 100)

        cmd_do = resolve(
            "BalanceTransfer.ChangeBalanceCommand", transfer.sender, -transfer.value
        )

        cmd_undo = resolve(
            "BalanceTransfer.ChangeBalanceCommand", transfer.sender, transfer.value
        )

        action = resolve("SimpleTransaction.CreateAction", cmd_do, cmd_undo)

        action.do()
        self.assertEqual(0, alice.current_balance)

        action.undo()
        self.assertEqual(100, alice.current_balance)

        action.do()
        self.assertEqual(0, alice.current_balance)

    def test_create_action_do_and_undo_command_tuple(self):
        alice = resolve("BalanceTransfer.CreateAccount", 100)
        bob = resolve("BalanceTransfer.CreateAccount", 100)
        transfer = resolve("BalanceTransfer.CreateTransferInfo", alice, bob, 100)

        cmd_do = resolve(
            "BalanceTransfer.ChangeBalanceCommand", transfer.sender, -transfer.value
        )

        cmd_undo = resolve(
            "BalanceTransfer.ChangeBalanceCommand", transfer.sender, transfer.value
        )

        cmd_tuple = (cmd_do, cmd_undo)

        action = resolve("SimpleTransaction.CreateAction", cmd_tuple)

        action.do()
        self.assertEqual(0, alice.current_balance)

        action.undo()
        self.assertEqual(100, alice.current_balance)

        action.do()
        self.assertEqual(0, alice.current_balance)

    def test_create_transaction_from_commands(self):
        alice = resolve("BalanceTransfer.CreateAccount", 100)
        bob = resolve("BalanceTransfer.CreateAccount", 100)
        transfer = resolve("BalanceTransfer.CreateTransferInfo", alice, bob, 100)

        transaction = resolve(
            "SimpleTransaction.CreateTransaction",
            [
                # 1
                resolve("BalanceTransfer.CheckSenderBalanceCommand", transfer),
                # 2
                (
                    resolve(
                        "BalanceTransfer.ChangeBalanceCommand",
                        transfer.sender,
                        -transfer.value,
                    ),
                    resolve(
                        "BalanceTransfer.ChangeBalanceCommand",
                        transfer.sender,
                        transfer.value,
                    ),
                ),
                # 3
                resolve("BalanceTransfer.CheckReceiverBalanceCommand", transfer),
                # 4
                (
                    resolve(
                        "BalanceTransfer.ChangeBalanceCommand",
                        transfer.receiver,
                        transfer.value,
                    ),
                    resolve(
                        "BalanceTransfer.ChangeBalanceCommand",
                        transfer.receiver,
                        -transfer.value,
                    ),
                ),
            ],
        )

        transaction()

        self.assertEqual(alice.current_balance, 0)
        self.assertEqual(bob.current_balance, 200)

    def test_create_transaction_from_commands_2(self):
        alice = resolve("BalanceTransfer.CreateAccount", 100)
        bob = resolve("BalanceTransfer.CreateAccount", 100)
        transfer = resolve("BalanceTransfer.CreateTransferInfo", alice, bob, 100)

        c1 = resolve("BalanceTransfer.CheckSenderBalanceCommand", transfer)
        c2_do = resolve(
            "BalanceTransfer.ChangeBalanceCommand",
            transfer.sender,
            -transfer.value,
        )
        c2_undo = resolve(
            "BalanceTransfer.ChangeBalanceCommand",
            transfer.sender,
            transfer.value,
        )
        c3 = resolve("BalanceTransfer.CheckReceiverBalanceCommand", transfer)
        c4_do = resolve(
            "BalanceTransfer.ChangeBalanceCommand",
            transfer.receiver,
            transfer.value,
        )
        c4_undo = resolve(
            "BalanceTransfer.ChangeBalanceCommand",
            transfer.receiver,
            -transfer.value,
        )

        transaction = resolve(
            "SimpleTransaction.CreateTransaction",
            [c1, (c2_do, c2_undo), c3, (c4_do, c4_undo)],
        )

        transaction()

        self.assertEqual(alice.current_balance, 0)
        self.assertEqual(bob.current_balance, 200)


@unittest.skip("refactoring")
class TestExecuteTransaction(unittest.TestCase):
    def setUp(self) -> None:
        resolve("Plugin.Load", "sturdy.extras.empty_command")()
        resolve("Plugin.Load", "sturdy.extras.simple_transaction")()
        resolve("Plugin.Load", "tests.mocks.plugins.balance_transfer")()

    def test_normal(self) -> None:
        alice = resolve("BalanceTransfer.CreateAccount", 100)
        bob = resolve("BalanceTransfer.CreateAccount", 100)
        transfer = resolve("BalanceTransfer.CreateTransferInfo", alice, bob, 100)

        transaction = resolve("BalanceTransfer.PerformBalanceTransferCommand", transfer)
        transaction()

        self.assertEqual(alice.current_balance, 0)
        self.assertEqual(bob.current_balance, 200)

    def test_fail_in_transaction_1(self) -> None:
        alice = resolve("BalanceTransfer.CreateAccount", 0)
        bob = resolve("BalanceTransfer.CreateAccount", 100)
        transfer = resolve("BalanceTransfer.CreateTransferInfo", alice, bob, 100)

        transaction = resolve("BalanceTransfer.PerformBalanceTransferCommand", transfer)
        transaction()

        self.assertEqual(alice.current_balance, 0)
        self.assertEqual(bob.current_balance, 100)

    def test_fail_in_transaction_2(self) -> None:
        alice = resolve("BalanceTransfer.CreateAccount", 100)
        bob = resolve("BalanceTransfer.CreateAccount", 1000)
        transfer = resolve("BalanceTransfer.CreateTransferInfo", alice, bob, 100)

        transaction = resolve("BalanceTransfer.PerformBalanceTransferCommand", transfer)
        transaction()

        self.assertEqual(alice.current_balance, 100)
        self.assertEqual(bob.current_balance, 1000)
